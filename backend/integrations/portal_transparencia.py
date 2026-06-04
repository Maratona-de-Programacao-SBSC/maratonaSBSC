import requests
import os
import zipfile
import io
from datetime import datetime, timedelta
from dotenv import load_dotenv
from services.importacoes import documento
from typing import Generator

load_dotenv()

TOKEN = os.getenv("PORTAL_TOKEN")

URL_NOTAS = "https://api.portaldatransparencia.gov.br/api-de-dados/notas-fiscais"
URL_NOTA_POR_CHAVE = "https://api.portaldatransparencia.gov.br/api-de-dados/notas-fiscais-por-chave"


def buscar_notas(pagina: int=1, cnpj: str =None) -> dict:
    if not cnpj:
        raise Exception("Informe um CNPJ")

    params = {"pagina": pagina, "cnpjEmitente": cnpj}
    headers = {"chave-api-dados": TOKEN}

    response = requests.get(URL_NOTAS, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.status_code}")

    return response.json()


def buscar_nota_por_chave(chave: str) -> dict:
    """
    Busca detalhes completos de uma NF-e pela chave de acesso.
    Retorna { notaFiscalDTO: {...}, itensNotaFiscal: [...] }
    """
    headers = {"chave-api-dados": TOKEN}
    params = {"chaveUnicaNotaFiscal": chave}

    response = requests.get(URL_NOTA_POR_CHAVE, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Erro ao buscar nota {chave}: {response.status_code}")

    return response.json()



def baixar_csv_path(data_inicio: str, data_fim: str, tipo: documento) -> Generator[str, None, None]:
    atual = datetime.strptime(data_inicio, "%Y%m%d").date()
    fim = datetime.strptime(data_fim, "%Y%m%d").date()


    while atual <= fim:
        data_str = atual.strftime("%Y%m%d")
        url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/despesas/{data_str}_Despesas.zip"

        response = requests.get(url)
        pasta = "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/"

        if response.status_code != 200:
            print(f"⚠️  Erro ao baixar despesas de {data_str}: {response.status_code}. Pulando.")
            atual += timedelta(days=1)
            continue

        
        zip_arquivo = zipfile.ZipFile(io.BytesIO(response.content))

        nome_csv = f"{data_str}_Despesas_{tipo.value}.csv"

        path = f"{pasta}{nome_csv}"

        zip_arquivo.extract(nome_csv, pasta)

        print(f"{data_str}Despesas baixadas e extraidas com sucesso")

        atual += timedelta(days=1)

        yield path
