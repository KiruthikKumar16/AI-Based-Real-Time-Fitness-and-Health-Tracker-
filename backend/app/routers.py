from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from .model_service import ensure_model
from .config import settings
from .database import get_db
from .models import Prediction
from .auth import get_current_user


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
def predict(payload: PredictRequest, data_dir: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    default_dir = Path(settings.data_dir)
    model = ensure_model(Path(data_dir) if data_dir else default_dir)
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

    # Store history
    record = Prediction(
        user_id=getattr(current_user, "id", None),
        age=payload.age,
        gender=payload.gender,
        height=payload.height,
        weight=payload.weight,
        duration=payload.duration,
        heart_rate=payload.heart_rate,
        body_temp=payload.body_temp,
        calories=pred,
    )
    db.add(record)
    db.commit()
    return PredictResponse(calories=pred)


@router.get("/history")
def get_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(Prediction)
    if getattr(current_user, "id", None) is not None:
        q = q.filter(Prediction.user_id == current_user.id)
    return [
        {
            "id": r.id,
            "calories": r.calories,
            "created_at": r.created_at.isoformat(),
            "age": r.age,
            "gender": r.gender,
            "height": r.height,
            "weight": r.weight,
            "duration": r.duration,
            "heart_rate": r.heart_rate,
            "body_temp": r.body_temp,
        }
        for r in q.order_by(Prediction.id.desc()).limit(50)
    ]


