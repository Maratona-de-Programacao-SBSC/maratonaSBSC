from repositories.testes_fraude import teste_sede_fantasma_repo, salvar_teste

def executar_teste():
    """
    Motor do teste: Identifica e penaliza CNPJs que compartilham 
    o mesmo endereço físico, um forte indício de empresas de fachada ou cartel.
    """
    print("[TESTE SEDE FANTASMA] Mapeando cruzamento de endereços físicos...")
    
    cnpjs = teste_sede_fantasma_repo.busca_sedes_compartilhadas()
    print(f"[TESTE SEDE FANTASMA] {len(cnpjs)} CNPJs operando em endereços aglomerados.")


    print(cnpjs[0])
    salvar_teste.salvar_falha(cnpjs, "teste_sede_fantasma")
        

    print(f"[TESTE SEDE FANTASMA] Concluído. {len(cnpjs)} CNPJs classificados como suspeitos.")