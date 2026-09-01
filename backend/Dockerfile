FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app/backend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY backend/ backend/

RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /uploads \
    && chown -R appuser:appuser /app /uploads

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
