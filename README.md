# Fault Classification API

Classifies maintenance text into one of five fault categories using a zero-shot NLP model.

## Architecture

```
Client → frontend:8000 → backend:8080 (internal only)
```

- **frontend** — public-facing FastAPI service. Validates the API key, then proxies the request to the backend.
- **backend** — internal FastAPI service. Loads a Hugging Face zero-shot-classification pipeline and returns the top predicted label.

Only the frontend is reachable from the host. The backend is on the internal Docker network with no published port.

## Running

```bash
docker compose up --build
```

The first run downloads the model (~250 MB). Subsequent starts use Docker's layer cache.

## Testing

```bash
curl -X POST http://localhost:8000/article/embed \
  -H "Content-Type: application/json" \
  -H "x-api-key: changeme" \
  -d '{"txt": "Pump impeller is worn and cavitating, causing vibration and reduced flow rate."}'
```

Example response:

```json
{
  "label": "mechanical",
  "score": 0.6949987411499023,
  "all": {
    "mechanical": 0.6949987411499023,
    "electrical": 0.1608951985836029,
    "other": 0.06739787012338638,
    "sensor": 0.05000130087137222,
    "software": 0.02670678310096264
  }
}
```

## Configuration

| Variable | Service | Default | Description |
|---|---|---|---|
| `API_KEY` | frontend | `changeme` | Key checked in `x-api-key` header |
| `MODEL_NAME` | backend | `typeform/distilbert-base-uncased-mnli` | HuggingFace model ID |
| `BACKEND_URL` | frontend | `http://backend:8080` | Internal backend address |

## Security

- **API key** — every request to the frontend must include a matching `x-api-key` header; mismatches return 401.
- **Backend not exposed** — the backend has no host port binding; it is only reachable from the frontend over the internal Docker network.
- **Input length cap** — text is rejected at 2000 characters by Pydantic before it reaches the model.
- **Non-root containers** — both images create and switch to a dedicated `appuser` before the process starts.
- **Config via env vars** — secrets and tunable values are passed in at runtime; nothing is hard-coded.
