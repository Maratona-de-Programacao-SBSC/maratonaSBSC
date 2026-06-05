from repositories.testes_fraude import teste_emp_fracionamento_repo

def executar_teste(ano: int):
    """
    Motor do teste: Identifica e penaliza CNPJs que utilizam a técnica
    de fracionamento de valores para burlar processos licitatórios.
    """
    print("[TESTE FRACIONAMENTO] Iniciando varredura de valores no teto da dispensa...")

    contador = 0
    
    alvos = teste_emp_fracionamento_repo.busca_empenhos_fracionados(ano)
    print(f"[TESTE FRACIONAMENTO] {len(alvos)} CNPJs suspeitos de burla de licitação encontrados.")

    for alvo in alvos:
        cnpj = alvo["cnpj"]
        qtd = alvo["qtd_empenhos"]
        valor_total = alvo["valor_total_suspeito"]
        
        # Penaliza no banco
        teste_emp_fracionamento_repo.salva_falha(cnpj)
        
        # Formatação amigável para o terminal
        moeda_br = f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        print(f"[TESTE FRACIONAMENTO] ALERTA MÁXIMO: CNPJ {cnpj} teve {qtd} empenhos no teto legal, somando {moeda_br}!")

        contador+=1

        if contador>=10:
            break

    print(f"[TESTE FRACIONAMENTO] Concluído. {len(alvos)} CNPJs classificados como suspeitos.")