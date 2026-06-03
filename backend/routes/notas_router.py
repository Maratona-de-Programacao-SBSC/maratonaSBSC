from fastapi import APIRouter, BackgroundTasks
# Em breve, colocaremos nossa lógica do ZIP dentro de um arquivo na pasta services
from services.processa_notas_zip import processar_lote_notas 

router = APIRouter(prefix="/notas", tags=["Notas Fiscais"])

@router.post("/importar-zip")
def importar_notas_zip(background_tasks: BackgroundTasks):
    """
    Processa o arquivo ZIP de Notas Fiscais e Itens local.
    Aplica ETL, Gatekeeper e salva usando o 'Set de Filtro' para ignorar itens suspeitos.
    """
    # Dispara a nossa estratégia original em background
    background_tasks.add_task(processar_lote_notas)
    
    return {
        "status": "Processamento em lote iniciado",
        "aviso": "O sistema está extraindo as notas e varrendo a base da BrasilAPI em background."
    }