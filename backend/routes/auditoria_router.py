from fastapi import APIRouter
from services.testes_fraude import teste_sede_fantasma
from services.testes_fraude import teste_emp_fracionamento
from services.testes_fraude import teste_saldo_empenho
from services.testes_fraude import teste_sazonalidade

router = APIRouter()



@router.post("/sede-fantasma")
def rodar_teste_sede_fantasma():
    """
    Dispara a varredura buscando múltiplas empresas registradas no mesmo CEP e Número.
    """
    teste_sede_fantasma.executar_teste()
    
    return {"status": "sucesso", "mensagem": "Teste de Sede Fantasma concluído com sucesso!"}


@router.post("/fracionamento-empenho")
def rodar_teste_fracionamento(ano: int):
    """
    Dispara a varredura de fracionamento de empenho para um ano específico.
    Exemplo: /auditoria/fracionamento-empenho?ano=2024
    """
    teste_emp_fracionamento.executar_teste(ano)
    
    return {
        "status": "sucesso", 
        "mensagem": f"Teste de Fracionamento de Empenho para o ano {ano} concluído!"
    }


@router.post("/saldo-empenho")
def rodar_teste_saldo_empenho():
    """
    Dispara a varredura para identificar pagamentos que excedem o valor empenhado.
    """
    teste_saldo_empenho.executar_teste()
    
    return {
        "status": "sucesso", 
        "mensagem": "Teste de Saldo de Empenho concluído com sucesso!"
    }


@router.post("/sazonalidade")
def rodar_teste_sazonalidade():
    """
    Dispara a varredura para identificar concentração atípica de liquidações em Dezembro.
    """
    teste_sazonalidade.executar_teste()
    
    return {
        "status": "sucesso", 
        "mensagem": "Teste de Sazonalidade concluído com sucesso!"
    }