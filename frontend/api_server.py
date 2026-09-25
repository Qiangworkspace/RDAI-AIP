import os
import httpx
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8080")
API_KEY = os.environ.get("API_KEY", "changeme")


class Article(BaseModel):
    txt: str = Field(..., max_length=2000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/article/embed")
async def embed_article(data: Article, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(f"{BACKEND_URL}/predict", json={"text": data.txt})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Model backend unavailable")
