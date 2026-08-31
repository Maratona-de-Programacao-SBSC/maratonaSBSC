from datetime import date
from unittest.mock import Mock

import pytest
import requests
from fastapi import HTTPException
from integrations import portal_transparencia as integracao_portal
from routes.importacao_router import _periodo
from services.importacoes.portal_transparencia import (
    gerar_anos_intervalos,
    gerar_datas,
    gerar_meses_intervalos,
)


def test_gerar_datas_inclui_limites() -> None:
    assert gerar_datas("20260130", "20260201") == ["20260130", "20260131", "20260201"]


def test_gerar_intervalos_mensais_sem_sobreposicao() -> None:
    assert list(gerar_meses_intervalos("20260115", "20260302")) == [
        ("20260115", "20260214"),
        ("20260215", "20260302"),
    ]


def test_gerar_intervalos_anuais_sem_sobreposicao() -> None:
    assert list(gerar_anos_intervalos("20240101", "20250102")) == [
        ("20240101", "20241231"),
        ("20250101", "20250102"),
    ]


def test_periodo_limita_quantidade_de_dias() -> None:
    with pytest.raises(HTTPException) as erro:
        _periodo(date(2024, 1, 1), date(2025, 1, 2), limite_dias=366)

    assert erro.value.status_code == 422


def test_periodo_rejeita_data_futura() -> None:
    with pytest.raises(HTTPException) as erro:
        _periodo(date(2099, 1, 1), date(2099, 1, 2), limite_dias=366)

    assert erro.value.status_code == 422
    assert "futuro" in erro.value.detail


@pytest.mark.parametrize("status_code", [403, 404])
def test_download_ignora_arquivo_ainda_nao_publicado(
    monkeypatch, tmp_path, status_code: int
) -> None:
    resposta = Mock(spec=requests.Response)
    resposta.status_code = status_code
    resposta.url = "https://dados.exemplo/arquivo.zip"
    monkeypatch.setenv("PASTA_UPLOAD_MYSQL", str(tmp_path))
    monkeypatch.setattr(integracao_portal, "_get", lambda *args, **kwargs: resposta)

    resultado = integracao_portal._baixar_e_extrair(resposta.url, "arquivo.csv")

    assert resultado is None
    resposta.close.assert_called_once_with()
