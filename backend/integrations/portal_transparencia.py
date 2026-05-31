import requests
import json
import os
import csv
import zipfile
import io
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("PORTAL_TOKEN")

URL = "https://api.portaldatransparencia.gov.br/api-de-dados/notas-fiscais"

def buscar_notas(pagina=1, cnpj=None):

    if not cnpj:
        raise Exception("Informe um CNPJ")

    params = {
        "pagina": pagina,
        "cnpjEmitente": cnpj
    }

    headers = {
        "chave-api-dados": TOKEN
    }

    response = requests.get(
        URL,
        params=params,
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.status_code}")

    dados = response.json()

    pasta = "dados/notas_portal"

    os.makedirs(pasta, exist_ok=True)

    with open(f"{pasta}/notas_pagina_{pagina}.json","w",encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    return dados



def busca_despesas_periodo(data_inicio: str, data_fim: str):
    atual = datetime.strptime(data_inicio, "%Y%m%d").date()
    fim = datetime.strptime(data_fim, "%Y%m%d").date()

    while atual <= fim:
        data_str = atual.strftime("%Y%m%d")

        url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/despesas/{data_str}_Despesas.zip"

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Erro na API: {response.status_code}")

        zip_arquivo = zipfile.ZipFile(io.BytesIO(response.content))

        pagamento = []
        empenho = []
        liquidacao = []
        pagamento_empenho = []
        empenho_liquidacao = []


        arquivos = {
            "Despesas_Pagamento.csv": pagamento,
            "Despesas_Empenho.csv": empenho,
            "Despesas_Liquidacao.csv": liquidacao,
            "Despesas_Pagamento_EmpenhosImpactados.csv": pagamento_empenho,
            "Despesas_Liquidacao_EmpenhosImpactados.csv": empenho_liquidacao,
            }


        for nome_csv in zip_arquivo.namelist():
            dados = None



            for sufixo, lista in arquivos.items():
                if nome_csv.endswith(sufixo):
                    dados = lista
                    break

            if dados is None: continue

            print(nome_csv)

            with zip_arquivo.open(nome_csv) as arquivo_csv:
                conteudo = io.TextIOWrapper(arquivo_csv, encoding="latin1")
                leitor = csv.DictReader(conteudo, delimiter=';')
                for linha in leitor:
                    dados.append(linha)

        
        yield pagamento, empenho, liquidacao, pagamento_empenho, empenho_liquidacao

        atual += timedelta(days=1)
