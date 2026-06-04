from repositories import database
from integrations import portal_transparencia
from enum import Enum


from schemes.empenho import PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA
from schemes.pagamento import PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA
from schemes.liquidacao import PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA


class documento(Enum):
    EMPENHOS = "Empenho"
    PAGAMENTOS = "Pagamento"
    LIQUIDACOES = "Liquidacao"


def importar_pagamentos_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:

    campos = gerar_campos(PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA["tabela"]

    for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, documento.PAGAMENTOS):
        database.salvar_csv(path, 
                            table_nome,
                            campos, 
                            set,
                            multithreading)
        

def importar_liquidacoes_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:

    campos = gerar_campos(PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA["tabela"]

    for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, documento.LIQUIDACOES):
        database.salvar_csv(path, 
                            table_nome,
                            campos, 
                            set, 
                            multithreading)
        

def importar_empenhos_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:

    campos = gerar_campos(PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA["tabela"]

    for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, documento.EMPENHOS):
        database.salvar_csv(path, 
                            table_nome,
                            campos, 
                            set,
                            multithreading)
        

def gerar_campos(schema: dict) -> str:
    total = schema["total_colunas"]
    mapa = schema["mapa"]
    campos = []

    for i in range(total):
        if i in mapa:
            info = mapa[i]
            if info["tipo"] in ["data", "valor"]:
                campos.append(f"@{info['coluna']}")
            else:
                campos.append(info["coluna"])
        else:
            campos.append(f"@lixo{i}")

    return ", ".join(campos)


def gerar_set(schema: dict) -> str:
    sets = []
    mapa = schema["mapa"]

    for info in mapa.values():
        col = info["coluna"]
        tipo = info["tipo"]

        if tipo == "data":
            sets.append(f"{col} = STR_TO_DATE(@{col}, '%d/%m/%Y')")

        elif tipo == "valor":
            sets.append(
                f"{col} = CAST(REPLACE(REPLACE(@{col}, '.', ''), ',', '.') AS DECIMAL(15,2))"
            )

    if not sets:
        return ""

    return "SET " + ", ".join(sets)

