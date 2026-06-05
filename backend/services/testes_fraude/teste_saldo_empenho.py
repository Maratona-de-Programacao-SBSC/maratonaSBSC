from repositories.testes_fraude import teste_saldo_emp_repo

def executar_teste():
    """
    Motor do teste: Identifica e penaliza empresas que receberam 
    valores totais acima do teto orçamentário empenhado para elas.
    """
    print("[TESTE SALDO GLOBAL] Iniciando análise de teto orçamentário por fornecedor...")

    counter=0
    
    alvos = teste_saldo_emp_repo.busca_cnpjs_com_saldo_estourado()
    print(f"[TESTE SALDO GLOBAL] {len(alvos)} CNPJs com inconsistência de saldo encontrados.")

    for alvo in alvos:
        cnpj = alvo["cnpj"]
        total_pago = alvo["total_pago"]
        total_empenhado = alvo["total_empenhado"]
        
        # Penaliza no banco
        teste_saldo_emp_repo.salva_falha(cnpj)
        
        # Formatação visual de moeda para o terminal
        moeda_pago = f"R$ {total_pago:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        moeda_emp = f"R$ {total_empenhado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        print(f"[TESTE SALDO GLOBAL] EXCESSO DE PAGAMENTO: O CNPJ {cnpj} recebeu um total de {moeda_pago}, "
              f"mas só tinha {moeda_emp} autorizados em empenhos!")
        
        counter+=1

        if counter>=10:
            break

    print(f"[TESTE SALDO GLOBAL] Concluído. {len(alvos)} CNPJs classificados como suspeitos.")