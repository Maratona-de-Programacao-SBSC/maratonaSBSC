from repositories.testes_fraude import teste_saldo_emp_repo, salvar_teste

def executar_teste():
    """
    Motor do teste: Identifica e penaliza empresas que receberam 
    valores totais acima do teto orçamentário empenhado para elas.
    """
    print("[TESTE SALDO GLOBAL] Iniciando análise de teto orçamentário por fornecedor...")

    
    cnpjs = teste_saldo_emp_repo.busca_cnpjs_com_saldo_estourado()
    print(f"[TESTE SALDO GLOBAL] {len(cnpjs)} CNPJs com inconsistência de saldo encontrados.")

    salvar_teste.salvar_falha(cnpjs, "teste_saldo_empenho")


    print(f"[TESTE SALDO GLOBAL] Concluído. {len(cnpjs)} CNPJs classificados como suspeitos.")