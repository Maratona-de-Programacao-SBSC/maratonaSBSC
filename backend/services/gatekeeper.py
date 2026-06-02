import requests
import time
import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

CACHE_FILE = "cache_cnpjs.json"


def carregar_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def salvar_cache(cache_dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_dict, f, indent=4)


CACHE_LOCAL = carregar_cache()


def buscar_data_abertura_cnpj(cnpj: str):
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()

    if cnpj_limpo in CACHE_LOCAL:
        return CACHE_LOCAL[cnpj_limpo]

    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
    print(f"[GATEKEEPER] Consultando CNPJ na BrasilAPI: {cnpj_limpo}...")

    headers = {"User-Agent": "Projeto_Transparencia/1.0 (Auditoria de Notas Fiscais)"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        time.sleep(2)

        if response.status_code == 200:
            dados = response.json()
            data_abertura = dados.get("data_inicio_atividade")
            CACHE_LOCAL[cnpj_limpo] = data_abertura
            salvar_cache(CACHE_LOCAL)
            return data_abertura

        elif response.status_code == 429:
            print("[GATEKEEPER] Rate limit atingido.")
            CACHE_LOCAL[cnpj_limpo] = "1900-01-01"
            salvar_cache(CACHE_LOCAL)
            return "1900-01-01"

        else:
            print(f"[GATEKEEPER] CNPJ não encontrado (Erro {response.status_code}).")
            CACHE_LOCAL[cnpj_limpo] = "1900-01-01"
            salvar_cache(CACHE_LOCAL)
            return "1900-01-01"

    except requests.exceptions.RequestException:
        print("[GATEKEEPER] Erro de conexão com BrasilAPI.")

    return "1900-01-01"


def executar_gatekeeper(nota: dict) -> str:
    """
    Valida a nota fiscal e retorna o status:
    - 'valida'    → empresa existia há mais de 3 meses antes da nota
    - 'suspeita'  → empresa emitiu nota nos primeiros 3 meses de existência
    - 'invalida'  → empresa não existia na data da nota
    """
    cnpj = nota.get("cnpjFornecedor", "")
    data_emissao_str = nota.get("dataEmissao", "")
    nome = nota.get("nomeFornecedor", "desconhecido")

    if not cnpj or not data_emissao_str:
        print(f"[GATEKEEPER] Nota sem CNPJ ou data de emissão. Descartando.")
        return "invalida"

    data_abertura_str = buscar_data_abertura_cnpj(cnpj)

    try:
        data_emissao_dt = datetime.strptime(data_emissao_str, "%d/%m/%Y")
        data_abertura_dt = datetime.strptime(data_abertura_str, "%Y-%m-%d")

        if data_emissao_dt < data_abertura_dt:
            print(f"[GATEKEEPER] INVÁLIDA: Nota de '{nome}' emitida antes da empresa existir!")
            print(f"Emissão: {data_emissao_str} | Abertura: {data_abertura_str}")
            return "invalida"

        if data_emissao_dt < data_abertura_dt + relativedelta(months=3):
            print(f"[GATEKEEPER] SUSPEITA: Nota de '{nome}' emitida nos primeiros 3 meses da empresa.")
            print(f"Emissão: {data_emissao_str} | Abertura: {data_abertura_str}")
            return "suspeita"

        return "valida"

    except ValueError as e:
        print(f"[GATEKEEPER] Erro ao comparar datas para '{nome}': {e}")
        return "invalida"