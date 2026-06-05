from repositories.testes_fraude import teste_sazonalidade_repo

def executar_teste():
    """
    Motor do teste: Identifica empresas que são ativadas apenas no final 
    do ano fiscal ("queima de orçamento" / restos a pagar).
    """
    print("[TESTE SAZONALIDADE] Analisando concentração de liquidações no fechamento do ano fiscal...")
    
    counter=0

    alvos = teste_sazonalidade_repo.busca_sazonalidade_suspeita()
    print(f"[TESTE SAZONALIDADE] {len(alvos)} CNPJs suspeitos de operar como 'queimadores de orçamento'.")

    for alvo in alvos:
        cnpj = alvo["cnpj"]
        total = alvo["total_liquidacoes"]
        dezembro = alvo["liquidacoes_dezembro"]
        porcentagem = (dezembro / total) * 100
        
        # Penaliza no banco
        teste_sazonalidade_repo.salva_falha(cnpj)
        
        print(f"[TESTE SAZONALIDADE] ALERTA DE FIM DE ANO: CNPJ {cnpj} teve {dezembro} de suas {total} liquidações ({porcentagem:.1f}%) registradas apenas em Dezembro!")

        counter+=1

        if counter >=10:
            break

    print(f"[TESTE SAZONALIDADE] Concluído. {len(alvos)} CNPJs classificados como suspeitos.")