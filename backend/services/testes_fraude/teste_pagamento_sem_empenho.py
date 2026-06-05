from repositories.testes_fraude import teste_pagamento_sem_empenho_repo

def executar_teste():
    """
    Motor do teste: Encontra CNPJs com pagamentos fantasmas (sem empenho) e penaliza.
    """
    print("[TESTE EMPENHO] Iniciando varredura de pagamentos sem empenho prévio...")

    contador = 0
    
    alvos = teste_pagamento_sem_empenho_repo.busca_pagamentos_sem_empenho()
    print(f"[TESTE EMPENHO] {len(alvos)} CNPJs suspeitos encontrados.")

    for alvo in alvos:
        cnpj = alvo["cnpj"]
        
        # Penaliza no banco
        teste_pagamento_sem_empenho_repo.salva_falha(cnpj)
        print(f"[TESTE EMPENHO] GRAVE: CNPJ {cnpj} recebeu pagamento sem ter empenho registrado!")

        contador+=1 

        if contador>=10:
            break

    print(f"[TESTE EMPENHO] Concluído. {len(alvos)} CNPJs classificados como suspeitos.")