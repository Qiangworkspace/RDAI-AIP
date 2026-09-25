import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from transformers import pipeline

MODEL_NAME = os.environ.get("MODEL_NAME", "typeform/distilbert-base-uncased-mnli")
LABELS = ["electrical", "mechanical", "software", "sensor", "other"]

app = FastAPI()
classifier = pipeline("zero-shot-classification", model=MODEL_NAME)


class PredictRequest(BaseModel):
    text: str = Field(..., max_length=2000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    result = classifier(req.text, LABELS)
    return {
        "label": result["labels"][0],
        "score": result["scores"][0],
        "all": dict(zip(result["labels"], result["scores"])),
    }
