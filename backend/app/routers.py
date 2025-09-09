from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .model_service import ensure_model


router = APIRouter()


class PredictRequest(BaseModel):
    age: int = Field(..., ge=1, le=120)
    gender: int = Field(..., ge=0, le=1, description="0 male, 1 female")
    height: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    duration: float = Field(..., ge=0)
    heart_rate: float = Field(..., ge=0)
    body_temp: float = Field(...)


class PredictResponse(BaseModel):
    calories: float


@router.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest, data_dir: Optional[str] = None):
    model = ensure_model(Path(data_dir) if data_dir else None)
    import pandas as pd

    row = {
        "Gender": payload.gender,
        "Age": payload.age,
        "Height": payload.height,
        "Weight": payload.weight,
        "Duration": payload.duration,
        "Heart_Rate": payload.heart_rate,
        "Body_Temp": payload.body_temp,
    }
    X = pd.DataFrame([row])
    try:
        pred = float(model.predict(X)[0])
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return PredictResponse(calories=pred)


