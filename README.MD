# Agoradit

Sistema para centralizacao e consulta de gastos governamentais. O backend importa dados publicos do Portal da Transparencia, armazena notas fiscais, empenhos, liquidacoes e pagamentos e disponibiliza consultas por CNPJ.

## Arquitetura

- FastAPI atende as consultas HTTP.
- MySQL armazena os dados importados.
- Redis atua como broker e backend de resultados.
- Celery executa as importacoes fora do processo web.
- Alembic aplica migrations versionadas antes da API e dos workers iniciarem.

As consultas usam um pool de conexoes por processo. Cada transacao recebe uma conexao isolada e executa `commit` ou `rollback` automaticamente.

## Execucao com Docker

Crie o arquivo de configuracao:

```bash
cp .env.example .env
```

Altere pelo menos `DATABASE_PASSWORD`, `ADMIN_API_KEY` e `PORTAL_TOKEN`. Em seguida:

```bash
docker compose up --build
```

Servicos disponiveis:

- frontend: `http://localhost`
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- liveness: `http://localhost:8000/health/live`
- readiness: `http://localhost:8000/health/ready`

O servico `migrate` executa `alembic upgrade head` automaticamente. Para criar uma nova migration:

```bash
docker compose run --rm migrate alembic revision -m "descricao"
```

## Desenvolvimento local

Requer Python 3.12 ou superior, MySQL e Redis.

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn main:app --app-dir backend --reload
```

Em outro terminal, inicie o worker:

```bash
celery --workdir backend -A worker.celery_app worker --loglevel=INFO
```

No Linux ou macOS, ative o ambiente com `source .venv/bin/activate`.

## Endpoints principais

Consultas publicas:

- `GET /cnpj/informacoes/{cnpj}`
- `GET /cnpj/despesas/{cnpj}/resumo`
- `GET /cnpj/despesas/{cnpj}/empenhos`
- `GET /cnpj/despesas/{cnpj}/liquidacoes`
- `GET /cnpj/despesas/{cnpj}/pagamentos`
- `GET /cnpj/notas/{cnpj}`
- `GET /cnpj/notas/{cnpj}/itens/{chave}`
- `GET /avaliacao/ranking`
- `POST /avaliacao/{cnpj}/votar`

Importacoes administrativas:

- `POST /importacao/cnpj`
- `POST /importacao/despesas?data_inicio=YYYY-MM-DD&data_fim=YYYY-MM-DD`
- `POST /importacao/notas?data_inicio=YYYY-MM-DD&data_fim=YYYY-MM-DD`
- `POST /importacao/itens-notas?data_inicio=YYYY-MM-DD&data_fim=YYYY-MM-DD`
- `GET /importacao/jobs/{job_id}`

Todas as rotas de importacao exigem o header:

```text
X-Admin-Key: valor-configurado-em-ADMIN_API_KEY
```

A criacao de uma importacao retorna HTTP `202`:

```json
{
  "job_id": "identificador-do-job",
  "status": "PENDING"
}
```

Use o identificador no endpoint de status para acompanhar a execucao.

## Escalabilidade

Os workers podem ser replicados sem aumentar a quantidade de processos da API:

```bash
docker compose up --scale worker=4
```

Para replicar a API em producao, coloque as instancias atras de um balanceador e remova o mapeamento fixo `8000:8000` do Compose. Ajuste `DATABASE_POOL_SIZE` considerando a soma de todos os processos web e workers para nao exceder o limite de conexoes do MySQL.

Os limites de periodo, pagina e tamanho de download podem ser configurados pelo `.env`. Downloads usam streaming, timeout e retry com backoff.

## Qualidade

```bash
ruff check backend
pytest --cov=backend --cov-report=term-missing
```

Os testes nao dependem de uma instancia real do MySQL ou Redis. Para validar a integracao completa, suba o ambiente pelo Docker Compose.
