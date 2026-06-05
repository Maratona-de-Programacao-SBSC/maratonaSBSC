from repositories.testes_fraude import teste_sede_fantasma_repo

def executar_teste():
    """
    Motor do teste: Identifica e penaliza CNPJs que compartilham 
    o mesmo endereço físico, um forte indício de empresas de fachada ou cartel.
    """
    print("[TESTE SEDE FANTASMA] Mapeando cruzamento de endereços físicos...")
    
    alvos = teste_sede_fantasma_repo.busca_sedes_compartilhadas()
    print(f"[TESTE SEDE FANTASMA] {len(alvos)} CNPJs operando em endereços aglomerados.")

    for alvo in alvos:
        cnpj = alvo["codigo_favorecido"]

        
        # Penaliza no banco
        teste_sede_fantasma_repo.salva_falha(cnpj)
        

    print(f"[TESTE SEDE FANTASMA] Concluído. {len(alvos)} CNPJs classificados como suspeitos.")