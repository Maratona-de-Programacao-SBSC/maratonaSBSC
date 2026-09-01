"""Cria o schema inicial.

Revision ID: 0001
Revises:
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _cnpj_valido(coluna: str) -> sa.CheckConstraint:
    return sa.CheckConstraint(
        f"LENGTH(TRIM({coluna})) > 0 "
        f"AND {coluna} NOT LIKE '%*%' "
        f"AND {coluna} REGEXP '^[0-9]{{14}}$'"
    )


def upgrade() -> None:
    op.create_table(
        "informacoes_cnpj",
        sa.Column("codigo_favorecido", sa.String(14), primary_key=True),
        sa.Column("razao_social", sa.String(255)),
        sa.Column("nome_fantasia", sa.String(255)),
        sa.Column("cod_cnae", sa.String(10)),
        sa.Column("cod_natjuridica", sa.String(10)),
        sa.Column("tipo_pessoa", sa.String(20)),
        sa.Column("logradouro", sa.String(255)),
        sa.Column("numero", sa.String(20)),
        sa.Column("complemento", sa.String(100)),
        sa.Column("cep", sa.String(8)),
        sa.Column("bairro", sa.String(100)),
        sa.Column("municipio", sa.String(100)),
        sa.Column("uf", sa.CHAR(2)),
    )
    op.create_index("idx_endereco", "informacoes_cnpj", ["municipio", "cep", "numero"])
    op.create_index("idx_cnae", "informacoes_cnpj", ["cod_cnae"])

    op.create_table(
        "notas_fiscais",
        sa.Column("chave_acesso", sa.String(44), primary_key=True),
        sa.Column("data_emissao", sa.Date),
        sa.Column("codigo_favorecido", sa.String(14), nullable=False),
        sa.Column("razao_social_emitente", sa.String(200)),
        sa.Column("uf_emitente", sa.CHAR(2)),
        sa.Column("municipio_emitente", sa.String(100)),
        sa.Column("codigo_orgao_destinatario", sa.Integer),
        sa.Column("orgao_destinatario", sa.String(200)),
        sa.Column("cnpj_destinatario", sa.String(14)),
        sa.Column("nome_destinatario", sa.String(200)),
        sa.Column("uf_destinatario", sa.CHAR(2)),
        sa.Column("destino_operacao", sa.SmallInteger),
        sa.Column("consumidor_final", sa.SmallInteger),
        sa.Column("valor", sa.Numeric(15, 2)),
        _cnpj_valido("codigo_favorecido"),
    )
    op.create_index("idx_codigo_favorecido", "notas_fiscais", ["codigo_favorecido", "data_emissao"])

    op.create_table(
        "itens_notas_fiscais",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "chave_nota",
            sa.String(44),
            sa.ForeignKey("notas_fiscais.chave_acesso", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("numero_produto", sa.String(10)),
        sa.Column("descricao", sa.String(300)),
        sa.Column("codigo_ncm", sa.String(10)),
        sa.Column("ncm", sa.String(300)),
        sa.Column("cfop", sa.String(10)),
        sa.Column("quantidade", sa.Numeric(15, 4)),
        sa.Column("unidade", sa.String(10)),
        sa.Column("valor_unitario", sa.Numeric(15, 4)),
        sa.Column("valor", sa.Numeric(15, 2)),
        sa.UniqueConstraint("chave_nota", "numero_produto", name="uq_item_nota"),
    )
    op.create_index("idx_chave_nota", "itens_notas_fiscais", ["chave_nota"])

    for tabela, chave, colunas in (
        (
            "empenhos",
            "codigo_empenho",
            [
                sa.Column("id_empenho", sa.BigInteger),
                sa.Column("data_emissao", sa.Date),
                sa.Column("tipo_empenho", sa.String(50)),
                sa.Column("codigo_orgao", sa.Integer),
                sa.Column("codigo_unidade_gestora", sa.Integer),
                sa.Column("codigo_favorecido", sa.String(14), nullable=False),
                sa.Column("favorecido", sa.String(200)),
                sa.Column("observacao", sa.Text),
                sa.Column("elemento_despesa", sa.String(20)),
                sa.Column("valor", sa.Numeric(15, 2)),
            ],
        ),
        (
            "liquidacoes",
            "codigo_liquidacao",
            [
                sa.Column("data_emissao", sa.Date),
                sa.Column("codigo_orgao", sa.Integer),
                sa.Column("codigo_unidade_gestora", sa.Integer),
                sa.Column("codigo_favorecido", sa.String(14), nullable=False),
                sa.Column("favorecido", sa.String(200)),
                sa.Column("observacao", sa.String(200)),
                sa.Column("codigo_elemento_despesa", sa.String(10)),
                sa.Column("valor", sa.Numeric(15, 2)),
            ],
        ),
        (
            "pagamentos",
            "codigo_pagamento",
            [
                sa.Column("data_emissao", sa.Date),
                sa.Column("codigo_favorecido", sa.String(14), nullable=False),
                sa.Column("favorecido", sa.String(200)),
                sa.Column("processo", sa.String(50)),
                sa.Column("codigo_unidade_gestora", sa.Integer),
                sa.Column("unidade_gestora", sa.String(200)),
                sa.Column("codigo_orgao", sa.Integer),
                sa.Column("orgao", sa.String(200)),
                sa.Column("observacao", sa.Text),
                sa.Column("valor", sa.Numeric(15, 2)),
            ],
        ),
    ):
        op.create_table(
            tabela,
            sa.Column(chave, sa.String(50), primary_key=True),
            *colunas,
            _cnpj_valido("codigo_favorecido"),
        )
        op.create_index(
            "idx_codigo_favorecido",
            tabela,
            ["codigo_favorecido", "data_emissao", "valor"],
        )

    op.create_table(
        "avaliacao_cnpjs",
        sa.Column("cnpj", sa.String(14), primary_key=True),
        sa.Column("votos_cidadaos", sa.Integer, nullable=False, server_default="0"),
        sa.CheckConstraint("votos_cidadaos >= 0", name="check_votos_nao_negativos"),
    )
    op.create_index("idx_ranking", "avaliacao_cnpjs", [sa.text("votos_cidadaos DESC")])


def downgrade() -> None:
    for tabela in (
        "avaliacao_cnpjs",
        "pagamentos",
        "liquidacoes",
        "empenhos",
        "itens_notas_fiscais",
        "notas_fiscais",
        "informacoes_cnpj",
    ):
        op.drop_table(tabela)
