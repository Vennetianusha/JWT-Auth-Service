from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, refresh_token
from app.routers import auth, api

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(api.router)


@app.get("/health")
def health():
    return {"status": "healthy"}