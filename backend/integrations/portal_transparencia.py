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


def buscar_despesas_periodo(data_inicio: str, data_fim: str):
    atual = datetime.strptime(data_inicio, "%Y%m%d").date()
    fim = datetime.strptime(data_fim, "%Y%m%d").date()


    buffer_pagamentos = []
    buffer_empenhos = []
    buffer_liquidacoes = []

    dias_acomulados = 0
    DIAS_ESPERADOS = 7

    while atual <= fim:
        data_str = atual.strftime("%Y%m%d")
        url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/despesas/{data_str}_Despesas.zip"

        response = requests.get(url)

        if response.status_code != 200:
            print(f"⚠️  Erro ao baixar despesas de {data_str}: {response.status_code}. Pulando.")
            atual += timedelta(days=1)
            continue


        zip_arquivo = zipfile.ZipFile(io.BytesIO(response.content))


        with zip_arquivo.open(f"{data_str}_Despesas_Pagamento.csv") as arquivo_csv:
            conteudo = io.TextIOWrapper(arquivo_csv, encoding="latin1")
            leitor = csv.DictReader(conteudo, delimiter=';')
            buffer_pagamentos.extend(leitor)


        with zip_arquivo.open(f"{data_str}_Despesas_Empenho.csv") as arquivo_csv:
            conteudo = io.TextIOWrapper(arquivo_csv, encoding="latin1")
            leitor = csv.DictReader(conteudo, delimiter=';')
            buffer_empenhos.extend(leitor)
    

        with zip_arquivo.open(f"{data_str}_Despesas_Liquidacao.csv") as arquivo_csv:
            conteudo = io.TextIOWrapper(arquivo_csv, encoding="latin1")
            leitor = csv.DictReader(conteudo, delimiter=';')
            buffer_liquidacoes.extend(leitor)


        print(f"{data_str}_Despesas_Pagamento.csv\n{data_str}_Despesas_Empenho.csv\n{data_str}_Despesas_Liquidacao.csv")

        dias_acomulados += 1

        if dias_acomulados >= DIAS_ESPERADOS:
            yield buffer_pagamentos, buffer_empenhos, buffer_liquidacoes
            buffer_pagamentos = []
            buffer_empenhos = []
            buffer_liquidacoes = []
            dias_acomulados = 0


        atual += timedelta(days=1)


    yield buffer_pagamentos, buffer_empenhos, buffer_liquidacoes


def baixar_csv_path(data_inicio: str, data_fim: str):
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

        nome_csv_pagamentos = f"{data_str}_Despesas_Pagamento.csv"
        nome_csv_liquidacoes = f"{data_str}_Despesas_Liquidacao.csv"
        nome_csv_empenhos = f"{data_str}_Despesas_Empenho.csv"

        path_pagamentos = f"{pasta}{nome_csv_pagamentos}"
        path_empenhos = f"{pasta}{nome_csv_empenhos}"
        path_liquidacoes = f"{pasta}{nome_csv_liquidacoes}"

        zip_arquivo.extract(nome_csv_pagamentos, pasta)
        zip_arquivo.extract(nome_csv_empenhos, pasta)
        zip_arquivo.extract(nome_csv_liquidacoes, pasta)

        print(f"{data_str}Despesas baixadas e extraidas com sucesso")

        atual += timedelta(days=1)

        yield path_pagamentos, path_empenhos, path_liquidacoes
