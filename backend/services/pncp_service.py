import requests
import json
import os


URL = "https://pncp.gov.br/api/search/"


def buscar_pncp(termo="informatica", pagina=1):

    params = {
        "q": termo,
        "pagina": pagina,
        "tamanhoPagina": 10
    }

    headers = {
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        URL,
        params=params,
        headers=headers,
        timeout=30
    )

    print(response.url)
    print(response.status_code)
    print(response.text[:500])

    if response.status_code != 200:
        raise Exception(f"Erro PNCP: {response.status_code}")

    try:
        dados = response.json()
    except:
        raise Exception("PNCP retornou HTML/bloqueio")

    pasta = "dados/pncp"

    os.makedirs(pasta, exist_ok=True)

    with open(
        f"{pasta}/busca_{termo}_pagina_{pagina}.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    return dados