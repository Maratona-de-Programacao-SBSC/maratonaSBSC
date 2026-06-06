from repositories.testes_fraude import teste_saldo_emp_repo

def executar_teste():
    """
    Motor do teste: Identifica e penaliza empresas que receberam 
    valores totais acima do teto orçamentário empenhado para elas.
    """
    print("[TESTE SALDO GLOBAL] Iniciando análise de teto orçamentário por fornecedor...")

    
    alvos = teste_saldo_emp_repo.busca_cnpjs_com_saldo_estourado()
    print(f"[TESTE SALDO GLOBAL] {len(alvos)} CNPJs com inconsistência de saldo encontrados.")

    for alvo in alvos:
        cnpj = alvo["codigo_favorecido"]
        
        # Penaliza no banco
        teste_saldo_emp_repo.salva_falha(cnpj)
        


    print(f"[TESTE SALDO GLOBAL] Concluído. {len(alvos)} CNPJs classificados como suspeitos.")