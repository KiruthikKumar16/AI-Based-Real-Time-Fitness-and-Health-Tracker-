from fastapi import FastAPI
from .routers import router as api_router


app = FastAPI(title="Fitness Calorie API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(api_router)


