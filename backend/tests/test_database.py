import pytest
from repositories import database


class ConexaoFalsa:
    def __init__(self) -> None:
        self.autocommit = None
        self.commits = 0
        self.rollbacks = 0
        self.fechada = False

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1

    def close(self) -> None:
        self.fechada = True


class PoolFalso:
    def __init__(self, conexao: ConexaoFalsa) -> None:
        self.conexao = conexao

    def get_connection(self) -> ConexaoFalsa:
        return self.conexao


def test_transacao_faz_commit(monkeypatch) -> None:
    conexao = ConexaoFalsa()
    monkeypatch.setattr(database, "_obter_pool", lambda: PoolFalso(conexao))

    with database._conexao(transacao=True):
        pass

    assert conexao.commits == 1
    assert conexao.rollbacks == 0
    assert conexao.fechada is True


def test_transacao_faz_rollback(monkeypatch) -> None:
    conexao = ConexaoFalsa()
    monkeypatch.setattr(database, "_obter_pool", lambda: PoolFalso(conexao))

    with pytest.raises(RuntimeError):
        with database._conexao(transacao=True):
            raise RuntimeError("falha")

    assert conexao.commits == 0
    assert conexao.rollbacks == 1
    assert conexao.fechada is True


@pytest.mark.parametrize("identificador", ["tabela; DROP TABLE x", "com espaco", "1tabela"])
def test_rejeita_identificador_sql_invalido(identificador: str) -> None:
    with pytest.raises(ValueError):
        database._validar_identificador(identificador)
