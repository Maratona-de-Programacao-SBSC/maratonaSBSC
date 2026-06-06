from repositories.testes_fraude import teste_sazonalidade_repo, salvar_teste

def executar_teste():
    """
    Motor do teste: Identifica empresas que são ativadas apenas no final 
    do ano fiscal ("queima de orçamento" / restos a pagar).
    """
    print("[TESTE SAZONALIDADE] Analisando concentração de liquidações no fechamento do ano fiscal...")


    cnpjs = teste_sazonalidade_repo.busca_sazonalidade_suspeita()
    print(f"[TESTE SAZONALIDADE] {len(cnpjs)} CNPJs suspeitos de operar como 'queimadores de orçamento'.")

 
    salvar_teste.salvar_falha(cnpjs, "teste_sazonalidade")
        
 
    print(f"[TESTE SAZONALIDADE] Concluído. {len(cnpjs)} CNPJs classificados como suspeitos.")