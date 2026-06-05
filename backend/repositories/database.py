import MySQLdb
import MySQLdb.cursors
import os
from concurrent.futures import ThreadPoolExecutor
import csv
from decimal import Decimal, InvalidOperation

HOST          = os.getenv("DATABASE_HOST")
USER          = os.getenv("DATABASE_USER")
PASSWORD      = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE")

# ── Conexão global (usada só para escritas/imports) ──────────────────────────
db = MySQLdb.connect(
    host=HOST, user=USER, passwd=PASSWORD, db=DATABASE_NAME, autocommit=False
)
cursor = db.cursor(MySQLdb.cursors.DictCursor)

_executor_banco = ThreadPoolExecutor(max_workers=1)


# ── Conexão isolada para leituras (thread-safe) ───────────────────────────────
def _nova_conexao():
    return MySQLdb.connect(
        host=HOST, user=USER, passwd=PASSWORD, db=DATABASE_NAME, autocommit=True,
        cursorclass=MySQLdb.cursors.DictCursor
    )

def busca_sql(query, params=None):
    conn = _nova_conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    finally:
        conn.close()

def busca_sql_um(query, params=None):
    conn = _nova_conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchone()
    finally:
        conn.close()


# ── Funções de escrita (mantém cursor global) ─────────────────────────────────
def salvar_csv(path: str, table_nome: str, campos: str, sets: str, multithreading: bool = False):
    def executar_insert():
        query = f"""
        LOAD DATA INFILE '{path}' IGNORE
        INTO TABLE {table_nome}
        CHARACTER SET latin1
        FIELDS TERMINATED BY ';'
        OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\\n'
        IGNORE 1 LINES
        ({campos})
        {sets}
        """
        cursor.execute(query)
        db.commit()
        os.remove(path)

    if multithreading:
        _executor_banco.submit(executar_insert)
    else:
        executar_insert()


def salvar_dict(table_nome: str, registros) -> None:
    if not registros:
        return

    dados = []
    for r in registros:
        if isinstance(r, dict):
            dados.append(r)
        elif hasattr(r, "__dict__"):
            dados.append(r.__dict__)
        else:
            raise ValueError(f"Tipo de registro não suportado: {type(r)}")

    if not dados:
        return

    colunas      = dados[0].keys()
    lista_colunas = ", ".join(colunas)
    placeholders  = ", ".join([f"%({col})s" for col in colunas])

    query = f"INSERT IGNORE INTO {table_nome} ({lista_colunas}) VALUES ({placeholders})"
    cursor.executemany(query, dados)
    db.commit()


def atualizar_campos_via_csv(path, table_nome, chave_primaria, chave_primaria_csv, multithreading=False, **kwargs):
    def executar_insert():
        colunas_bd  = list(kwargs.keys())
        colunas_csv = list(kwargs.values())

        set_clause        = ", ".join([f"{col} = %s" for col in colunas_bd])
        null_clause_list  = [f"({col} IS NULL OR {col} = 0)" for col in colunas_bd]
        null_clause       = " AND ".join(null_clause_list)
        query = f"UPDATE {table_nome} SET {set_clause} WHERE {chave_primaria} = %s AND {null_clause}"

        dados_para_atualizar = []
        with open(path, mode='r', encoding='latin1') as f:
            reader = csv.DictReader(f, delimiter=';')
            for linha in reader:
                valor_chave = linha.get(chave_primaria_csv)
                if valor_chave:
                    valores = []
                    for coluna in colunas_csv:
                        valor = linha.get(coluna)
                        try:
                            valor = Decimal(valor.replace('.', '').replace(',', '.'))
                        except (InvalidOperation, AttributeError):
                            pass
                        valores.append(valor)
                    dados_para_atualizar.append(tuple(valores + [valor_chave]))

        if dados_para_atualizar:
            cursor.executemany(query, dados_para_atualizar)
            db.commit()

    if multithreading:
        _executor_banco.submit(executar_insert)
    else:
        executar_insert()


def busca_cnpj(cnpj: str, table_nome: str, dataclass) -> list:
    rows = busca_sql(f"SELECT * FROM {table_nome} WHERE codigo_favorecido = %s", (cnpj,))
    return [dataclass(**d) for d in rows]


def busca_cnpj_dado(cnpj: str, table_nome: str, nome_dado: str) -> list:
    rows = busca_sql(f"SELECT {nome_dado} FROM {table_nome} WHERE codigo_favorecido = %s", (cnpj,))
    return [row[nome_dado] for row in rows]


def fechar_threads() -> None:
    _executor_banco.shutdown(wait=False, cancel_futures=True)
    if 'db' in globals():
        try:
            cursor.close()
            db.close()
        except:
            pass
    print("Esteira e conexão fechadas. Saindo...")