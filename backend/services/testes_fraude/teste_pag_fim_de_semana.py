from repositories.testes_fraude import teste_pag_fim_de_semana_repo

def executar_teste():
    """
    Motor do teste: Encontra pagamentos realizados em Sábados ou Domingos e penaliza.
    """
    print("[TESTE FIM DE SEMANA] Iniciando varredura de pagamentos fora de dias úteis...")

    contador = 0
    
    alvos = teste_pag_fim_de_semana_repo.busca_pagamentos_fim_de_semana()
    total = len(alvos)
    print(f"[TESTE FIM DE SEMANA] {total} CNPJs/CPFs suspeitos encontrados.")

    for alvo in alvos:
        cnpj = alvo["cnpj"]
        
        # Penaliza no banco
        teste_pag_fim_de_semana_repo.salva_falha(cnpj)
        print(f"[TESTE FIM DE SEMANA] GRAVE: {cnpj} recebeu pagamento no fim de semana!")

        contador+=1

        if contador >=10:
            break

    print(f"[TESTE FIM DE SEMANA] Concluído. {total} CNPJs penalizados no banco.")