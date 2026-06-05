from fastapi import APIRouter
from services.testes_fraude import teste_pagamento_sem_empenho
from services.testes_fraude import teste_pag_fim_de_semana
from services.testes_fraude import teste_sede_fantasma

router = APIRouter()

@router.post("/pagamento-sem-empenho")
def rodar_teste_pagamento_sem_empenho():
    """
    Dispara a varredura no banco buscando pagamentos que não possuem empenho prévio.
    """
    # Você precisará ter uma função executora no seu arquivo do serviço
    teste_pagamento_sem_empenho.executar_teste()
    
    return {"status": "sucesso", "mensagem": "Teste de Pagamento sem Empenho concluído. Verifique a tabela avaliacao_cnpjs!"}


@router.post("/pagamento-fim-de-semana")
def rodar_teste_pagamento_fim_de_semana():
    """
    Dispara a varredura buscando pagamentos realizados fora de dias úteis (Sábado e Domingo).
    """
    teste_pag_fim_de_semana.executar_teste()
    
    return {"status": "sucesso", "mensagem": "Teste de Pagamentos em Fim de Semana concluído com sucesso!"}


@router.post("/sede-fantasma")
def rodar_teste_sede_fantasma():
    """
    Dispara a varredura buscando múltiplas empresas registradas no mesmo CEP e Número.
    """
    teste_sede_fantasma.executar_teste()
    
    return {"status": "sucesso", "mensagem": "Teste de Sede Fantasma concluído com sucesso!"}