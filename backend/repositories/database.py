import MySQLdb
import os
from concurrent.futures import ThreadPoolExecutor

HOST = os.getenv("DATABASE_HOST")
USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE")

db = MySQLdb.connect(
    host=HOST,
    user=USER,
    passwd=PASSWORD,
    db=DATABASE_NAME,
    autocommit=False,
)

cursor = db.cursor(MySQLdb.cursors.DictCursor)

_executor_banco = ThreadPoolExecutor(max_workers=1)

def salvar_csv(path: str, table_nome: str, campos: str, sets: str, multithreading: bool=False) -> None:

    # ==========================================================
    # Permite inserir o csv diratemente na database, bom
    # para grande quantidades de dados
    # ==========================================================

    def executar_insert():
        query = f"""
        LOAD DATA INFILE '{path}' IGNORE
        INTO TABLE {table_nome}
        CHARACTER SET latin1
        FIELDS TERMINATED BY ';'
        OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (
            {campos}
        )
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
    
    colunas = dados[0].keys()
    
    lista_colunas = ", ".join(colunas)
    placeholders = ", ".join([f"%({coluna})s" for coluna in colunas])
    
    query = f"""
        INSERT IGNORE INTO {table_nome} ({lista_colunas})
        VALUES ({placeholders})
    """
    
    cursor.executemany(query, dados)
    db.commit()

    
def busca_cnpj(cnpj: str, table_nome: str, dataclass) -> None:
    query = f"""SELECT * FROM {table_nome} WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = cursor.fetchall()

    return [dataclass(**d) for d in dados]


def busca_cnpj_dado(cnpj: str, table_nome: str, nome_dado: str) -> None:
    query = f"""SELECT {nome_dado} FROM {table_nome} WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = [row[nome_dado] for row in cursor.fetchall()]

    return dados;


def fechar_esteira() -> None:
    _executor_banco.shutdown(wait=True)