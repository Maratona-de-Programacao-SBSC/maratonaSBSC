import csv
import os
import re
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from mysql.connector import pooling

_IDENTIFICADOR = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_pool: pooling.MySQLConnectionPool | None = None
_pool_lock = threading.Lock()


def _inteiro_ambiente(nome: str, padrao: int) -> int:
    try:
        return int(os.getenv(nome, str(padrao)))
    except ValueError as exc:
        raise RuntimeError(f"A variavel {nome} precisa ser um inteiro") from exc


def _obter_pool() -> pooling.MySQLConnectionPool:
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                _pool = pooling.MySQLConnectionPool(
                    pool_name=f"agoradit_{os.getpid()}",
                    pool_size=_inteiro_ambiente("DATABASE_POOL_SIZE", 10),
                    pool_reset_session=True,
                    host=os.getenv("DATABASE_HOST", "localhost"),
                    port=_inteiro_ambiente("DATABASE_PORT", 3306),
                    user=os.getenv("DATABASE_USER"),
                    password=os.getenv("DATABASE_PASSWORD"),
                    database=os.getenv("DATABASE"),
                    connection_timeout=_inteiro_ambiente("DATABASE_CONNECT_TIMEOUT", 10),
                    allow_local_infile=True,
                )
    return _pool


def _validar_identificador(valor: str) -> str:
    if not _IDENTIFICADOR.fullmatch(valor):
        raise ValueError(f"Identificador SQL invalido: {valor!r}")
    return valor


@contextmanager
def _conexao(*, transacao: bool = False) -> Iterator[Any]:
    conn = _obter_pool().get_connection()
    try:
        conn.autocommit = not transacao
        yield conn
        if transacao:
            conn.commit()
    except Exception:
        if transacao:
            conn.rollback()
        raise
    finally:
        conn.close()


def verificar_conexao() -> bool:
    with _conexao() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone()[0] == 1


def busca_sql(query: str, params: tuple | None = None) -> list[dict]:
    with _conexao() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()


def busca_sql_um(query: str, params: tuple | None = None) -> dict | None:
    with _conexao() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()


def executar_sql(query: str, params: tuple | None = None) -> int:
    with _conexao(transacao=True) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.rowcount


def salvar_csv(path: str, table_nome: str, campos: str, sets: str) -> None:
    tabela = _validar_identificador(table_nome)
    arquivo = Path(path).resolve()
    query = f"""
        LOAD DATA LOCAL INFILE %s IGNORE
        INTO TABLE {tabela}
        CHARACTER SET latin1
        FIELDS TERMINATED BY ';'
        OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\\n'
        IGNORE 1 LINES
        ({campos})
        {sets}
    """

    try:
        with _conexao(transacao=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (str(arquivo),))
    finally:
        arquivo.unlink(missing_ok=True)


def salvar_dict(table_nome: str, registros: list[Any]) -> None:
    if not registros:
        return

    dados = []
    for registro in registros:
        if isinstance(registro, dict):
            dados.append(registro)
        elif hasattr(registro, "__dict__"):
            dados.append(vars(registro))
        else:
            raise ValueError(f"Tipo de registro nao suportado: {type(registro)}")

    tabela = _validar_identificador(table_nome)
    colunas = [_validar_identificador(coluna) for coluna in dados[0]]
    lista_colunas = ", ".join(colunas)
    placeholders = ", ".join([f"%({coluna})s" for coluna in colunas])
    query = f"INSERT IGNORE INTO {tabela} ({lista_colunas}) VALUES ({placeholders})"

    with _conexao(transacao=True) as conn:
        with conn.cursor() as cursor:
            cursor.executemany(query, dados)


def atualizar_campos_via_csv(
    path: str,
    table_nome: str,
    chave_primaria: str,
    chave_primaria_csv: str,
    **kwargs: str,
) -> None:
    arquivo = Path(path).resolve()
    tabela = _validar_identificador(table_nome)
    chave = _validar_identificador(chave_primaria)
    colunas_bd = [_validar_identificador(coluna) for coluna in kwargs]
    colunas_csv = list(kwargs.values())
    dados = []

    try:
        with arquivo.open(mode="r", encoding="latin1") as stream:
            reader = csv.DictReader(stream, delimiter=";")
            for linha in reader:
                valor_chave = linha.get(chave_primaria_csv)
                if not valor_chave:
                    continue
                valores: list[Any] = [valor_chave]
                for coluna in colunas_csv:
                    valor: Any = linha.get(coluna)
                    try:
                        valor = Decimal(valor.replace(".", "").replace(",", "."))
                    except (InvalidOperation, AttributeError):
                        pass
                    valores.append(valor)
                dados.append(tuple(valores))

        if not dados:
            return

        todas_colunas = [chave, *colunas_bd]
        placeholders = ", ".join(["%s"] * len(todas_colunas))
        definicoes = ", ".join([f"{coluna} DECIMAL(15,2)" for coluna in colunas_bd])
        set_clause = ", ".join([f"t.{coluna} = tmp.{coluna}" for coluna in colunas_bd])
        null_clause = " AND ".join(
            [f"(t.{coluna} IS NULL OR t.{coluna} = 0)" for coluna in colunas_bd]
        )

        with _conexao(transacao=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DROP TEMPORARY TABLE IF EXISTS tmp_update")
                cursor.execute(
                    f"CREATE TEMPORARY TABLE tmp_update "
                    f"({chave} VARCHAR(64) NOT NULL, {definicoes})"
                )
                insert_sql = (
                    f"INSERT INTO tmp_update ({', '.join(todas_colunas)}) VALUES ({placeholders})"
                )
                for inicio in range(0, len(dados), 1000):
                    cursor.executemany(insert_sql, dados[inicio : inicio + 1000])
                cursor.execute(f"ALTER TABLE tmp_update ADD INDEX idx_chave ({chave})")
                cursor.execute(
                    f"UPDATE {tabela} t JOIN tmp_update tmp ON t.{chave} = tmp.{chave} "
                    f"SET {set_clause} WHERE {null_clause}"
                )
    finally:
        arquivo.unlink(missing_ok=True)


def busca_cnpj(cnpj: str, table_nome: str, dataclass: type) -> list[Any]:
    tabela = _validar_identificador(table_nome)
    rows = busca_sql(f"SELECT * FROM {tabela} WHERE codigo_favorecido = %s", (cnpj,))
    return [dataclass(**row) for row in rows]


def busca_cnpj_dado(cnpj: str, table_nome: str, nome_dado: str) -> list[Any]:
    tabela = _validar_identificador(table_nome)
    coluna = _validar_identificador(nome_dado)
    rows = busca_sql(f"SELECT {coluna} FROM {tabela} WHERE codigo_favorecido = %s", (cnpj,))
    return [row[coluna] for row in rows]
