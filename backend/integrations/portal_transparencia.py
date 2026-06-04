import requests
import os
import zipfile
import io
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from schemes.documento import Documento
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



def baixar_csv_path(data_inicio: str, data_fim: str, tipo: Documento) -> Generator[str, None, None]:


    atual = datetime.strptime(data_inicio, "%Y%m%d").date()
    fim = datetime.strptime(data_fim, "%Y%m%d").date()


    while atual <= fim:
        data_str = atual.strftime("%Y%m%d")
        mes_str = atual.strftime("%Y%m")


        if tipo in [Documento.NOTA_FISCAL, Documento.ITEM_NOTA_FISCAL]:
            incremento = relativedelta(months=1)
        else:
            incremento = relativedelta(days=1)


        if tipo == Documento.NOTA_FISCAL:
            url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/nfe/{mes_str}_NFe.zip"
            nome_csv = f"{mes_str}_NFe_NotaFiscal.csv"
        elif tipo == Documento.ITEM_NOTA_FISCAL:
            url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/nfe/{mes_str}_NFe.zip"
            nome_csv = f"{mes_str}_NFe_NotaFiscalItem.csv"
        else:
            url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/despesas/{data_str}_Despesas.zip"
            nome_csv = f"{data_str}_Despesas_{tipo.value}.csv"

        response = requests.get(url)
        pasta = "D:/ProgramData/MySQL/MySQL Server 9.5/Uploads/"

        if response.status_code != 200:
            print(f"⚠️  Erro ao baixar {data_str}: {response.status_code}. Pulando.")
            atual += incremento
            continue
        

        zip_arquivo = zipfile.ZipFile(io.BytesIO(response.content))
        path = f"{pasta}{nome_csv}"
        zip_arquivo.extract(nome_csv, pasta)

        print(f"{data_str} Documento {tipo} baixado e extraído com sucesso")
        

        atual += incremento
        yield path


def baixar_csv_cnpj():
    ano_mes_atual = datetime.now()
    ano_mes_atual -= relativedelta(months=1)
    ano_mes_atual = ano_mes_atual.strftime("%Y%m")

    url = f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/favorecidos-pj/{ano_mes_atual}_FavorecidosPJ.zip"
    nome_csv = f"{ano_mes_atual}_CNPJ.csv"

    response = requests.get(url)
    pasta = "D:/ProgramData/MySQL/MySQL Server 9.5/Uploads/"

    if response.status_code != 200:
        print(f"⚠️  Erro ao baixar {ano_mes_atual}: {response.status_code}. Pulando.")
        return
    

    zip_arquivo = zipfile.ZipFile(io.BytesIO(response.content))
    path = f"{pasta}{nome_csv}"
    zip_arquivo.extract(nome_csv, pasta)

    print(f"{ano_mes_atual} Documento INFORMACOES_CNPJ baixado e extraído com sucesso")
    

    return path