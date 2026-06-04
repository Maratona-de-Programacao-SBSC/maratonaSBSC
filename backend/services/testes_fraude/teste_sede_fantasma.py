from repositories import teste_sede_fantasma_repo

def executar_teste():
    """
    Motor do teste: Identifica e penaliza CNPJs que compartilham 
    o mesmo endereço físico, um forte indício de empresas de fachada ou cartel.
    """
    print("[TESTE SEDE FANTASMA] Mapeando cruzamento de endereços físicos...")
    
    alvos = teste_sede_fantasma_repo.busca_sedes_compartilhadas()
    print(f"[TESTE SEDE FANTASMA] {len(alvos)} CNPJs operando em endereços aglomerados.")

    for alvo in alvos:
        cnpj = alvo["cnpj"]
        razao_social = alvo["razao_social"]
        logradouro = alvo["logradouro"]
        numero = alvo["numero"]
        qtd_empresas = alvo["qtd_empresas"]
        
        # Penaliza no banco
        teste_sede_fantasma_repo.salva_falha(cnpj)
        
        print(f"[TESTE SEDE FANTASMA] CARTEL?: A empresa '{razao_social}' (CNPJ: {cnpj}) divide o endereço "
              f"({logradouro}, {numero}) com outras {qtd_empresas - 1} empresas fornecedoras!")

    print(f"[TESTE SEDE FANTASMA] Concluído. {len(alvos)} CNPJs classificados como suspeitos.")