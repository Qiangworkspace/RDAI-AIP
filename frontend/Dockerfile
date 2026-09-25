FROM python:3.11-slim

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_server.py .

RUN chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
