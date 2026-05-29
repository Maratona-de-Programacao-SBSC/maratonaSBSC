import requests
import json
import os

URL = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"

def buscar_contratos(data_inicial: str, data_final: str, modalidade: int = 5, pagina: int = 1, tamanho: int = 10):
    params = {
        "dataInicial": data_inicial,
        "dataFinal": data_final,
        "codigoModalidadeContratacao": modalidade,
        "pagina": pagina,
        "tamanhoPagina": tamanho,
    }

    response = requests.get(URL, params=params)

    if response.status_code != 200:
        raise Exception(f"Erro na API PNCP: {response.status_code}")

    data = response.json()
    salvar_contratos(data, pagina)
    return data

def salvar_contratos(dados, pagina: int):
    pasta = "dados/contratos_pncp"
    os.makedirs(pasta, exist_ok=True)

    with open(f"{pasta}/contratos_pagina_{pagina}.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)