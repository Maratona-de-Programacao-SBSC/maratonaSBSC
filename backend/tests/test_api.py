from unittest.mock import Mock

from fastapi.testclient import TestClient
from main import app

client = TestClient(app, raise_server_exceptions=False)


def test_health_live() -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_rejeita_cnpj_invalido() -> None:
    response = client.get("/cnpj/informacoes/123")

    assert response.status_code == 422


def test_limita_tamanho_da_pagina() -> None:
    response = client.get("/cnpj/despesas/12345678000199/empenhos", params={"tamanho": 101})

    assert response.status_code == 422


def test_importacao_exige_chave_administrativa(monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEY", "segredo")

    response = client.post("/importacao/cnpj")

    assert response.status_code == 401


def test_importacao_retorna_job(monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEY", "segredo")
    resultado = Mock(id="job-123")
    delay = Mock(return_value=resultado)
    monkeypatch.setattr("routes.importacao_router.importar_despesas.delay", delay)

    response = client.post(
        "/importacao/despesas",
        params={"data_inicio": "2026-01-01", "data_fim": "2026-01-31"},
        headers={"X-Admin-Key": "segredo"},
    )

    assert response.status_code == 202
    assert response.json() == {"job_id": "job-123", "status": "PENDING"}
    delay.assert_called_once_with("20260101", "20260131")


def test_rejeita_periodo_invertido(monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEY", "segredo")

    response = client.post(
        "/importacao/despesas",
        params={"data_inicio": "2026-02-01", "data_fim": "2026-01-01"},
        headers={"X-Admin-Key": "segredo"},
    )

    assert response.status_code == 422
    assert "data_fim" in response.json()["detail"]


def test_erro_interno_nao_expoe_detalhes(monkeypatch) -> None:
    def falhar(*args, **kwargs):
        raise RuntimeError("senha-do-banco")

    monkeypatch.setattr("routes.dados_router.busca_sql_um", falhar)

    response = client.get("/cnpj/informacoes/12345678000199")

    assert response.status_code == 500
    assert response.json() == {"detail": "Erro interno do servidor"}
    assert "senha-do-banco" not in response.text
