import requests
import os
import csv
import zipfile
import io
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("PORTAL_TOKEN")

URL_NOTAS = "https://api.portaldatransparencia.gov.br/api-de-dados/notas-fiscais"
URL_NOTA_POR_CHAVE = "https://api.portaldatransparencia.gov.br/api-de-dados/notas-fiscais-por-chave"


def buscar_notas(pagina=1, cnpj=None):
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


def busca_despesas_periodo(data_inicio: str, data_fim: str):
    atual = datetime.strptime(data_inicio, "%Y%m%d").date()
    fim = datetime.strptime(data_fim, "%Y%m%d").date()

    while atual <= fim:
        data_str = atual.strftime("%Y%m%d")
        url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/despesas/{data_str}_Despesas.zip"

        response = requests.get(url)

        if response.status_code != 200:
            print(f"⚠️  Erro ao baixar despesas de {data_str}: {response.status_code}. Pulando.")
            atual += timedelta(days=1)
            continue

        zip_arquivo = zipfile.ZipFile(io.BytesIO(response.content))

        pagamentos = []
        empenhos = []
        liquidacoes = []
        pagamentos_empenhos = []
        empenhos_liquidacoes = []

        arquivos = {
            "Despesas_Pagamento.csv": pagamentos,
            "Despesas_Empenho.csv": empenhos,
            "Despesas_Liquidacao.csv": liquidacoes,
            "Despesas_Pagamento_EmpenhosImpactados.csv": pagamentos_empenhos,
            "Despesas_Liquidacao_EmpenhosImpactados.csv": empenhos_liquidacoes,
        }

        for nome_csv in zip_arquivo.namelist():
            dados = None
            for sufixo, lista in arquivos.items():
                if nome_csv.endswith(sufixo):
                    dados = lista
                    break
            if dados is None:
                continue
            print(nome_csv)
            with zip_arquivo.open(nome_csv) as arquivo_csv:
                conteudo = io.TextIOWrapper(arquivo_csv, encoding="latin1")
                leitor = csv.DictReader(conteudo, delimiter=';')
                for linha in leitor:
                    dados.append(linha)

        yield pagamentos, empenhos, liquidacoes, pagamentos_empenhos, empenhos_liquidacoes

        atual += timedelta(days=1)