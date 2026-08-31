import logging
import os
import shutil
import tempfile
import threading
import uuid
import zipfile
from collections.abc import Generator
from datetime import datetime
from pathlib import Path

import requests
from dateutil.relativedelta import relativedelta
from requests.adapters import HTTPAdapter
from schemes.documento import Documento
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)
URL_NOTAS = "https://api.portaldatransparencia.gov.br/api-de-dados/notas-fiscais"
URL_NOTA_POR_CHAVE = "https://api.portaldatransparencia.gov.br/api-de-dados/notas-fiscais-por-chave"
_thread_local = threading.local()


def _inteiro_ambiente(nome: str, padrao: int) -> int:
    try:
        return int(os.getenv(nome, str(padrao)))
    except ValueError as exc:
        raise RuntimeError(f"A variavel {nome} precisa ser um inteiro") from exc


def _sessao() -> requests.Session:
    if not hasattr(_thread_local, "sessao"):
        retry = Retry(
            total=_inteiro_ambiente("PORTAL_HTTP_RETRIES", 4),
            backoff_factor=1,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET",),
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
        sessao = requests.Session()
        sessao.mount("https://", adapter)
        _thread_local.sessao = sessao
    return _thread_local.sessao


def _get(url: str, **kwargs) -> requests.Response:
    timeout = (
        _inteiro_ambiente("PORTAL_CONNECT_TIMEOUT", 10),
        _inteiro_ambiente("PORTAL_READ_TIMEOUT", 120),
    )
    return _sessao().get(url, timeout=timeout, **kwargs)


def _headers_api() -> dict[str, str]:
    token = os.getenv("PORTAL_TOKEN")
    if not token:
        raise RuntimeError("PORTAL_TOKEN nao configurado")
    return {"chave-api-dados": token}


def buscar_notas(pagina: int = 1, cnpj: str | None = None) -> dict:
    if not cnpj:
        raise ValueError("Informe um CNPJ")
    response = _get(
        URL_NOTAS,
        params={"pagina": pagina, "cnpjEmitente": cnpj},
        headers=_headers_api(),
    )
    response.raise_for_status()
    return response.json()


def buscar_nota_por_chave(chave: str) -> dict:
    response = _get(
        URL_NOTA_POR_CHAVE,
        params={"chaveUnicaNotaFiscal": chave},
        headers=_headers_api(),
    )
    response.raise_for_status()
    return response.json()


def _pasta_upload() -> Path:
    valor = os.getenv("PASTA_UPLOAD_MYSQL")
    if not valor:
        raise RuntimeError("PASTA_UPLOAD_MYSQL nao configurada")
    pasta = Path(valor).resolve()
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def _baixar_e_extrair(url: str, nome_csv: str) -> Path | None:
    pasta = _pasta_upload()
    max_download = _inteiro_ambiente("PORTAL_MAX_DOWNLOAD_BYTES", 2_000_000_000)
    max_csv = _inteiro_ambiente("PORTAL_MAX_CSV_BYTES", 8_000_000_000)
    response = _get(url, stream=True)
    if response.status_code in (403, 404):
        logger.warning("Arquivo ainda nao publicado: %s", url)
        response.close()
        return None
    response.raise_for_status()

    tamanho = int(response.headers.get("Content-Length", 0))
    if tamanho and tamanho > max_download:
        raise RuntimeError(f"Download excede o limite configurado: {url}")

    temporario: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=pasta, suffix=".zip", delete=False) as stream:
            temporario = Path(stream.name)
            baixados = 0
            for bloco in response.iter_content(chunk_size=1024 * 1024):
                if not bloco:
                    continue
                baixados += len(bloco)
                if baixados > max_download:
                    raise RuntimeError(f"Download excede o limite configurado: {url}")
                stream.write(bloco)

        with zipfile.ZipFile(temporario) as arquivo_zip:
            try:
                info = arquivo_zip.getinfo(nome_csv)
            except KeyError as exc:
                raise RuntimeError(f"CSV esperado nao encontrado no ZIP: {nome_csv}") from exc
            if info.file_size > max_csv:
                raise RuntimeError(f"CSV excede o limite configurado: {nome_csv}")

            destino = pasta / f"{uuid.uuid4().hex}_{Path(nome_csv).name}"
            with arquivo_zip.open(info) as origem, destino.open("wb") as saida:
                shutil.copyfileobj(origem, saida, length=1024 * 1024)
            return destino
    finally:
        response.close()
        if temporario is not None:
            temporario.unlink(missing_ok=True)


def baixar_csv_path(data_inicio: str, data_fim: str, tipo: Documento) -> Generator[str, None, None]:
    atual = datetime.strptime(data_inicio, "%Y%m%d").date()
    fim = datetime.strptime(data_fim, "%Y%m%d").date()
    if fim < atual:
        raise ValueError("data_fim deve ser igual ou posterior a data_inicio")

    while atual <= fim:
        data_str = atual.strftime("%Y%m%d")
        mes_str = atual.strftime("%Y%m")
        incremento = (
            relativedelta(months=1)
            if tipo in (Documento.NOTA_FISCAL, Documento.ITEM_NOTA_FISCAL)
            else relativedelta(days=1)
        )

        if tipo == Documento.NOTA_FISCAL:
            url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/nfe/{mes_str}_NFe.zip"
            nome_csv = f"{mes_str}_NFe_NotaFiscal.csv"
        elif tipo == Documento.ITEM_NOTA_FISCAL:
            url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/nfe/{mes_str}_NFe.zip"
            nome_csv = f"{mes_str}_NFe_NotaFiscalItem.csv"
        else:
            url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/despesas/{data_str}_Despesas.zip"
            nome_csv = f"{data_str}_Despesas_{tipo.value}.csv"

        destino = _baixar_e_extrair(url, nome_csv)
        atual += incremento
        if destino is not None:
            logger.info("Documento %s baixado para o periodo %s", tipo.value, data_str)
            yield str(destino)


def baixar_csv_cnpj() -> str:
    ano_mes = (datetime.now() - relativedelta(months=1)).strftime("%Y%m")
    url = (
        "https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/"
        f"favorecidos-pj/{ano_mes}_FavorecidosPJ.zip"
    )
    destino = _baixar_e_extrair(url, f"{ano_mes}_CNPJ.csv")
    if destino is None:
        raise RuntimeError(f"Arquivo de CNPJ nao publicado para {ano_mes}")
    return str(destino)
