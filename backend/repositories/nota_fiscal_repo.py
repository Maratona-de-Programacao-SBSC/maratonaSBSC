from repositories.database import cursor, db


def salvar(detalhes: dict, status: str = "valida"):
    nota = detalhes.get("notaFiscalDTO", {})
    itens = detalhes.get("itensNotaFiscal", [])

    _salvar_nota(nota, status)
    _salvar_itens(nota.get("chaveNotaFiscal"), itens)

    db.commit()


# AVISO DO VICTOR, ESSE MONTE DE SALVAR SEPARADO N É BACANA
# NÃO APAGUEI POR MEDO, USAR AS FUNÇOES DO DATABASE.PY


def _salvar_nota(nota: dict, status: str):
    query = """
        INSERT IGNORE INTO notas_fiscais (
            chave_acesso, data_emissao, cpf_cnpj_emitente,
            razao_social_emitente, codigo_orgao_destinatario,
            orgao_destinatario, valor, status
        ) VALUES (
            %(chave_acesso)s, %(data_emissao)s, %(cpf_cnpj_emitente)s,
            %(razao_social_emitente)s, %(codigo_orgao_destinatario)s,
            %(orgao_destinatario)s, %(valor)s, %(status)s
        )
    """

    dados = {
        "chave_acesso": nota.get("chaveNotaFiscal"),
        "data_emissao": _formatar_data(nota.get("dataEmissao")),
        "cpf_cnpj_emitente": nota.get("cnpjFornecedor", "").replace(".", "").replace("/", "").replace("-", ""),
        "razao_social_emitente": nota.get("nomeFornecedor"),
        "codigo_orgao_destinatario": nota.get("codigoOrgaoDestinatario"),
        "orgao_destinatario": nota.get("orgaoDestinatario"),
        "valor": _formatar_valor(nota.get("valorNotaFiscal", "0")),
        "status": status,
    }

    cursor.execute(query, dados)


def _salvar_itens(chave: str, itens: list):
    if not itens:
        return

    query = """
        INSERT IGNORE INTO itens_notas_fiscais (
            chave_nota, numero_produto, descricao, codigo_ncm,
            ncm, cfop, quantidade, unidade, valor_unitario, valor
        ) VALUES (
            %(chave_nota)s, %(numero_produto)s, %(descricao)s, %(codigo_ncm)s,
            %(ncm)s, %(cfop)s, %(quantidade)s, %(unidade)s, %(valor_unitario)s, %(valor)s
        )
    """

    dados = [
        {
            "chave_nota": chave,
            "numero_produto": item.get("numeroProduto"),
            "descricao": item.get("descricaoProdutoServico"),
            "codigo_ncm": item.get("codigoNcmSh"),
            "ncm": item.get("ncmSh"),
            "cfop": item.get("cfop"),
            "quantidade": _formatar_valor(item.get("quantidade", "0")),
            "unidade": item.get("unidade"),
            "valor_unitario": _formatar_valor(item.get("valorUnitario", "0")),
            "valor": _formatar_valor(item.get("valor", "0")),
        }
        for item in itens
    ]

    cursor.executemany(query, dados)


def _formatar_data(data_str: str):
    if not data_str:
        return None
    try:
        from datetime import datetime
        return datetime.strptime(data_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def _formatar_valor(valor_str: str) -> float:
    try:
        return float(valor_str.replace(".", "").replace(",", "."))
    except (ValueError, AttributeError):
        return 0.0