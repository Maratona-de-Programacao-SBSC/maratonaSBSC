from repositories import teste_pag_fim_de_semana_repo

def executar_teste():
    """
    Motor do teste: Pega os suspeitos no banco que receberam em finais de semana e salva as falhas.
    """
    print("[TESTE FDS] Iniciando varredura de pagamentos em dias não úteis...")
    
    alvos = teste_pag_fim_de_semana_repo.busca_pagamentos_fim_de_semana()
    print(f"[TESTE FDS] {len(alvos)} transações suspeitas encontradas.")

    for alvo in alvos:
        cnpj = alvo["cnpj"]
        
        # Como o SQL já fez 100% do filtro, só precisamos penalizar o CNPJ
        teste_pag_fim_de_semana_repo.salva_falha(cnpj)
        print(f"[TESTE FDS] ANOMALIA: CNPJ {cnpj} recebeu pagamento em um final de semana!")

    print(f"[TESTE FDS] Concluído. {len(alvos)} CNPJs classificados como suspeitos.")