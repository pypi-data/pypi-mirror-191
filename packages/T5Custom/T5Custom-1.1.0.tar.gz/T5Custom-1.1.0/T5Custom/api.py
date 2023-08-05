#  Created By Sushil
from fastapi import FastAPI
from pydantic import BaseModel

from load_model import load_model

app = FastAPI()

model = load_model()


class Request(BaseModel):
    description: str


class PredictionResponse(BaseModel):
    sentences: str
    Usecase: str


@app.post("/predict/", response_model=PredictionResponse)
async def predict(request: Request, model: model):
    result = model.predict(request.description)
    return PredictionResponse(
        sentences= request.description, Usecase = result
    )
