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


def importar_pagamentos_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:

    campos = gerar_campos(PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA["tabela"]

    for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.PAGAMENTOS):
        database.salvar_csv(path, 
                            table_nome,
                            campos, 
                            set,
                            multithreading)
        
    if multithreading: database.aguardar_executor()

def importar_liquidacoes_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:


    
    campos = gerar_campos(PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA["tabela"]

    for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.LIQUIDACOES):
        database.salvar_csv(path, 
                            table_nome,
                            campos, 
                            set, 
                            multithreading)     
   

    table_nome = PORTAL_TRANSPARENCIA_LIQUIDACAO_EMPENHOS_SCHEMA["tabela"]

    if multithreading: database.aguardar_executor()

    for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.LIQUIDACAO_EMPENHOS):
            database.atualizar_campos_via_csv(
                                        path,
                                        table_nome="liquidacoes",
                                        chave_primaria="codigo_liquidacao",
                                        chave_primaria_csv="Código Liquidação",
                                        multithreading=True,
                                        valor="Valor Liquidado (R$)"
                                    )
            
    if multithreading: database.aguardar_executor()
    
def importar_empenhos_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:

    campos = gerar_campos(PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA["tabela"]


    for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.EMPENHOS):
        database.salvar_csv(path, 
                            table_nome,
                            campos, 
                            set,
                            multithreading)
        

    if multithreading: database.aguardar_executor()
        

def importar_notas_fiscais_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:
    campos = gerar_campos(PORTAL_TRANSPARENCIA_NOTA_FISCAL_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_NOTA_FISCAL_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_NOTA_FISCAL_SCHEMA["tabela"]


    for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.NOTA_FISCAL):
        database.salvar_csv(path, 
                            table_nome,
                            campos, 
                            set,
                            multithreading)
        
    if multithreading: database.aguardar_executor()   

def importar_itens_notas_fiscais_csv(data_inicio: str, data_fim: str, multithreading: bool) -> None:
    campos = gerar_campos(PORTAL_TRANSPARENCIA_ITEM_NOTA_FISCAL_SCHEMA)
    set = gerar_set(PORTAL_TRANSPARENCIA_ITEM_NOTA_FISCAL_SCHEMA)
    table_nome = PORTAL_TRANSPARENCIA_ITEM_NOTA_FISCAL_SCHEMA["tabela"]

    for path in portal_transparencia.baixar_csv_path(data_inicio, data_fim, Documento.ITEM_NOTA_FISCAL):
        database.salvar_csv(path, 
                            table_nome,
                            campos, 
                            set,
                            multithreading)
        
    if multithreading: database.aguardar_executor()
        

def importar_informacoes_cnpj_csv(multithreading: bool) -> None:
    campos = gerar_campos(PORTA_TRANSPARENCIA_INFORMACOES_CNPJ_SCHEMA)
    set = gerar_set(PORTA_TRANSPARENCIA_INFORMACOES_CNPJ_SCHEMA)
    table_nome = PORTA_TRANSPARENCIA_INFORMACOES_CNPJ_SCHEMA["tabela"]


    path = portal_transparencia.baixar_csv_cnpj()
    database.salvar_csv(path, 
                        table_nome,
                        campos, 
                        set,
                        multithreading)
    
    if multithreading: database.aguardar_executor()
        

def gerar_campos(schema: dict) -> str:
    total = schema["total_colunas"]
    mapa = schema["mapa"]
    campos = []

    for i in range(total):
        if i in mapa:
            info = mapa[i]
            if info["tipo"] in ["data", "valor", "substitui"]:
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

    if not sets: return ""

    return "SET " + ", ".join(sets)

