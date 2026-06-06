from repositories.database import db, cursor



def salvar_falha(cnpj_dict, campo_teste: str) -> None:
    query = (
        "INSERT INTO avaliacao_cnpjs "
        f"(cnpj, {campo_teste}, score_automatico, score_total, data_ultima_auditoria) "
        "VALUES (%(codigo_favorecido)s, 1, 1, 1, CURRENT_DATE()) "
        f"ON DUPLICATE KEY UPDATE "
        f"{campo_teste} = 1, "
        "score_automatico = score_automatico + 1, "
        "score_total = score_total + 1, "
        "data_ultima_auditoria = CURRENT_DATE()"
    )
    cursor.executemany(query, cnpj_dict)
    db.commit()