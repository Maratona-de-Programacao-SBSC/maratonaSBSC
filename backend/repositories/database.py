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
def salvar_csv(path: str, table_nome: str, campos: str, sets: str):

    print(f"Salvando: {path}")
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


def atualizar_campos_via_csv(path, table_nome, chave_primaria, chave_primaria_csv, **kwargs):
    print(f"Salvando: {path}")
    colunas_bd  = list(kwargs.keys())
    colunas_csv = list(kwargs.values())

    dados = []
    with open(path, mode='r', encoding='latin1') as f:
        reader = csv.DictReader(f, delimiter=';')
        for linha in reader:
            valor_chave = linha.get(chave_primaria_csv)
            if not valor_chave:
                continue
            valores = [valor_chave]
            for coluna in colunas_csv:
                valor = linha.get(coluna)
                try:
                    valor = Decimal(valor.replace('.', '').replace(',', '.'))
                except (InvalidOperation, AttributeError):
                    pass
                valores.append(valor)
            dados.append(tuple(valores))

    if not dados:
        os.remove(path)
        return

    todas_colunas = [chave_primaria] + colunas_bd
    placeholders  = ", ".join(["%s"] * len(todas_colunas))
    set_clause    = ", ".join([f"t.{col} = tmp.{col}" for col in colunas_bd])
    null_clause   = " AND ".join([f"(t.{col} IS NULL OR t.{col} = 0)" for col in colunas_bd])

    cursor.execute("DROP TEMPORARY TABLE IF EXISTS tmp_update")
    cursor.execute(f"""
        CREATE TEMPORARY TABLE tmp_update (
            {chave_primaria} VARCHAR(64) NOT NULL,
            {", ".join([f"{col} DECIMAL(15,2)" for col in colunas_bd])}
        )
    """)

    insert_sql = f"INSERT INTO tmp_update ({', '.join(todas_colunas)}) VALUES ({placeholders})"
    try:
        cursor.executemany(insert_sql, dados)
    except MySQLdb.OperationalError:
        for i in range(0, len(dados), 1000):
            cursor.executemany(insert_sql, dados[i:i + 1000])

    cursor.execute(f"ALTER TABLE tmp_update ADD INDEX idx_chave ({chave_primaria})")

    cursor.execute(f"""
        UPDATE {table_nome} t
        JOIN tmp_update tmp ON t.{chave_primaria} = tmp.{chave_primaria}
        SET {set_clause}
        WHERE {null_clause}
    """)

    db.commit()
    os.remove(path)




def busca_cnpj(cnpj: str, table_nome: str, dataclass) -> list:
    rows = busca_sql(f"SELECT * FROM {table_nome} WHERE codigo_favorecido = %s", (cnpj,))
    return [dataclass(**d) for d in rows]


def busca_cnpj_dado(cnpj: str, table_nome: str, nome_dado: str) -> list:
    rows = busca_sql(f"SELECT {nome_dado} FROM {table_nome} WHERE codigo_favorecido = %s", (cnpj,))
    return [row[nome_dado] for row in rows]


