from fastapi import APIRouter
from integrations.portal_transparencia import buscar_notas, buscar_nota_por_chave
from services.gatekeeper import executar_gatekeeper
from repositories import nota_fiscal_repo

router = APIRouter(prefix="/notas", tags=["Notas Fiscais"])


@router.get("/")
def listar_notas(cnpj: str, pagina: int = 1):
    """
    Busca notas por CNPJ, valida com o gatekeeper e salva no banco.

    Status possíveis:
    - valida    → empresa existia há mais de 3 meses antes da nota
    - suspeita  → empresa emitiu nota nos primeiros 3 meses de existência
    - invalida  → empresa não existia na data da nota (não salva)
    """
    notas = buscar_notas(pagina=pagina, cnpj=cnpj)

    validas = 0
    suspeitas = 0
    invalidas = 0

    for nota in notas:
        status = executar_gatekeeper(nota)

        if status == "invalida":
            invalidas += 1
            continue  # não salva no banco

        chave = nota.get("chaveNotaFiscal")

        try:
            detalhes = buscar_nota_por_chave(chave)
            nota_fiscal_repo.salvar(detalhes, status=status)

            if status == "valida":
                validas += 1
            else:
                suspeitas += 1

        except Exception as e:
            print(f"⚠️  Erro ao buscar/salvar nota {chave}: {e}")

    return {
        "pagina": pagina,
        "total_recebidas": len(notas),
        "validas": validas,
        "suspeitas": suspeitas,
        "invalidas": invalidas,
    }