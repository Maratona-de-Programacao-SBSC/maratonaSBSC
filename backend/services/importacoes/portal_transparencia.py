from repositories import database
from integrations import portal_transparencia
from schemes.documento import Documento


from schemes.empenho import PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA
from schemes.pagamento import PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA
from schemes.liquidacao import PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA
from schemes.nota_fiscal import PORTAL_TRANSPARENCIA_NOTA_FISCAL_SCHEMA 
from schemes.item_nota_fiscal import PORTAL_TRANSPARENCIA_ITEM_NOTA_FISCAL_SCHEMA
from schemes.informacoes_cnpj import PORTA_TRANSPARENCIA_INFORMACOES_CNPJ_SCHEMA
from schemes.liquidacao import PORTAL_TRANSPARENCIA_LIQUIDACAO_EMPENHOS_SCHEMA

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time


def gerar_datas(data_inicio, data_fim):
    atual = datetime.strptime(data_inicio, "%Y%m%d").date()
    fim   = datetime.strptime(data_fim,    "%Y%m%d").date()
    datas = []
    while atual <= fim:
        datas.append(atual.strftime("%Y%m%d"))
        atual += relativedelta(days=1)

    return datas


def gerar_meses(data_inicio, data_fim):
    atual = datetime.strptime(data_inicio, "%Y%m%d").date()
    fim   = datetime.strptime(data_fim,    "%Y%m%d").date()
    meses = []
    while atual <= fim:
        meses.append(atual.strftime("%Y%m%d"))
        atual += relativedelta(months=1)
    return meses


def importar_pagamentos_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:
    campos = gerar_campos(PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA["tabela"]

    if not multithreading:
        for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.PAGAMENTOS):
            database.salvar_csv(path, table_nome, campos, set)
        return
    

    def baixar(data_str):
        path = list(portal_transparencia.baixar_csv_path(data_str, data_str, Documento.PAGAMENTOS))
        time.sleep(0.5)
        return path
    
    datas = gerar_datas(data_inicio, data_fim)

    with ThreadPoolExecutor(max_workers=3) as pool:
        paths = [p for ps in pool.map(baixar, datas) for p in ps]

    for path in paths:
        database.salvar_csv(path, table_nome, campos, set)
        


def importar_liquidacoes_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:
    campos = gerar_campos(PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA)
    table_nome1 = PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA["tabela"]
    table_nome2 = PORTAL_TRANSPARENCIA_LIQUIDACAO_EMPENHOS_SCHEMA["tabela"]

    if not multithreading:
        for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.LIQUIDACOES):
            database.salvar_csv(path, table_nome1, campos, set)

        for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.LIQUIDACAO_EMPENHOS):
            database.atualizar_campos_via_csv(path, table_nome=table_nome2, chave_primaria="codigo_liquidacao", chave_primaria_csv="Código Liquidação", valor="Valor Liquidado (R$)")

        return


    def baixar(data_str):
        paths = list(portal_transparencia.baixar_csv_path(data_str, data_str, Documento.LIQUIDACOES))
        time.sleep(0.5)
        return paths

    with ThreadPoolExecutor(max_workers=3) as pool:
        paths = [p for ps in pool.map(baixar, gerar_datas(data_inicio, data_fim)) for p in ps]

    for path in paths:
        database.salvar_csv(path, table_nome1, campos, set)

    def baixar_empenhos(data_str):
        paths = list(portal_transparencia.baixar_csv_path(data_str, data_str, Documento.LIQUIDACAO_EMPENHOS))
        time.sleep(0.5)
        return paths

    with ThreadPoolExecutor(max_workers=3) as pool:
        paths = [p for ps in pool.map(baixar_empenhos, gerar_datas(data_inicio, data_fim)) for p in ps]

    for path in paths:
        database.atualizar_campos_via_csv(path, table_nome=table_nome2, chave_primaria="codigo_liquidacao", chave_primaria_csv="Código Liquidação", valor="Valor Liquidado (R$)")


def importar_empenhos_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:
    campos = gerar_campos(PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA["tabela"]

    if not multithreading:
        for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.EMPENHOS):
            database.salvar_csv(path, table_nome, campos, set)
        return

    def baixar(data_str):
        path = list(portal_transparencia.baixar_csv_path(data_str, data_str, Documento.EMPENHOS))
        time.sleep(0.5)
        return path

    with ThreadPoolExecutor(max_workers=3) as pool:
        paths = [p for ps in pool.map(baixar, gerar_datas(data_inicio, data_fim)) for p in ps]

    for path in paths:
        database.salvar_csv(path, table_nome, campos, set)


def importar_notas_fiscais_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:
    campos = gerar_campos(PORTAL_TRANSPARENCIA_NOTA_FISCAL_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_NOTA_FISCAL_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_NOTA_FISCAL_SCHEMA["tabela"]

    if not multithreading:
        for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.NOTA_FISCAL):
            database.salvar_csv(path, table_nome, campos, set)
        return

    def baixar(data_str):
        path = list(portal_transparencia.baixar_csv_path(data_str, data_str, Documento.NOTA_FISCAL))
        time.sleep(0.5)
        return path

    with ThreadPoolExecutor(max_workers=3) as pool:
        paths = [p for ps in pool.map(baixar, gerar_meses(data_inicio, data_fim)) for p in ps]

    for path in paths:
        database.salvar_csv(path, table_nome, campos, set)


def importar_itens_notas_fiscais_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:
    campos = gerar_campos(PORTAL_TRANSPARENCIA_ITEM_NOTA_FISCAL_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_ITEM_NOTA_FISCAL_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_ITEM_NOTA_FISCAL_SCHEMA["tabela"]

    if not multithreading:
        for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.ITEM_NOTA_FISCAL):
            database.salvar_csv(path, table_nome, campos, set)
        return

    def baixar(data_str):
        path = list(portal_transparencia.baixar_csv_path(data_str, data_str, Documento.ITEM_NOTA_FISCAL))
        time.sleep(0.5)
        return path

    with ThreadPoolExecutor(max_workers=3) as pool:
        paths = [p for ps in pool.map(baixar, gerar_meses(data_inicio, data_fim)) for p in ps]

    for path in paths:
        database.salvar_csv(path, table_nome, campos, set)


def importar_informacoes_cnpj_csv(multithreading: bool) -> None:
    campos = gerar_campos(PORTA_TRANSPARENCIA_INFORMACOES_CNPJ_SCHEMA)
    set = gerar_set(PORTA_TRANSPARENCIA_INFORMACOES_CNPJ_SCHEMA)
    table_nome = PORTA_TRANSPARENCIA_INFORMACOES_CNPJ_SCHEMA["tabela"]

    path = portal_transparencia.baixar_csv_cnpj()
    database.salvar_csv(path, table_nome, campos, set)
        

def gerar_campos(schema: dict) -> str:
    total = schema["total_colunas"]
    mapa = schema["mapa"]
    campos = []

    for i in range(total):
        if i in mapa:
            info = mapa[i]
            if info["tipo"] in ["data", "valor", "substitui", "cnpj"]:
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
        elif tipo == "cnpj":
                    # 1. Limpeza de caracteres especiais
                    limpeza = f"REPLACE(REPLACE(REPLACE(@{col}, '.', ''), '-', ''), '/', '')"
                    # 2. Padronização com 14 dígitos e zeros à esquerda
                    padronizado = f"LPAD({limpeza}, 14, '0')"
                    
                    # 3. Lógica de descarte: se tem asterisco ou é vazio, retorna NULL
                    # Como a coluna aceita NULL (ou o trigger barrou antes), o banco entende o formato
                    sets.append(
                        f"{col} = CASE "
                        f"WHEN @{col} LIKE '%*%' OR TRIM(@{col}) = '' THEN NULL "
                        f"ELSE {padronizado} "
                        f"END"
                    )

    if not sets: return ""

    result = "SET " + ", ".join(sets)
    print(result)
    return result

