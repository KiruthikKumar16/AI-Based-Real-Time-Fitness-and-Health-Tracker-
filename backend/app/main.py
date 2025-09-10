from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .routers import router as api_router
from .database import Base, engine, get_db
from .models import User
from .auth import Token, authenticate_user, create_access_token, get_current_user, get_password_hash
from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI(title="Fitness Calorie API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.post("/auth/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        return {"detail": "Username already exists"}
    user = User(username=username, password_hash=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}


@app.post("/auth/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return {"access_token": "", "token_type": "bearer"}
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


