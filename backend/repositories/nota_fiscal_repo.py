from repositories import database

# ==========================================
# NOVAS FUNÇÕES (Para consultas limpas)
# ==========================================

def busca_chave(chave_acesso: str) -> dict:
    """Busca uma nota fiscal específica pela chave de acesso."""
    query = """SELECT * FROM notas_fiscais WHERE chave_acesso = %s"""
    database.cursor.execute(query, (chave_acesso,))
    return database.cursor.fetchone()

def busca_itens(chave_acesso: str) -> list:
    """Busca todos os itens de uma nota fiscal específica."""
    query = """SELECT * FROM itens_notas_fiscais WHERE chave_nota = %s"""
    database.cursor.execute(query, (chave_acesso,))
    return database.cursor.fetchall()

#Pronto! Sem inserts duplicados, sem gambiarras. Se no futuro precisarmos salvar uma nota única pelo painel, usamos o database.salvar_dict)