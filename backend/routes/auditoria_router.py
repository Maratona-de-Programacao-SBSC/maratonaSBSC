from fastapi import APIRouter
from services.testes_fraude import teste_pagamento_sem_empenho

router = APIRouter()

@router.post("/pagamento-sem-empenho")
def rodar_teste_pagamento_sem_empenho():
    """
    Dispara a varredura no banco buscando pagamentos que não possuem empenho prévio.
    """
    # Você precisará ter uma função executora no seu arquivo do serviço
    teste_pagamento_sem_empenho.executar_teste()
    
    return {"status": "sucesso", "mensagem": "Teste de Pagamento sem Empenho concluído. Verifique a tabela avaliacao_cnpjs!"}