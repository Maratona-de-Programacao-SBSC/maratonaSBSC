import requests
import json
import os

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

    with open(
        f"{pasta}/notas_pagina_{pagina}.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    return dados