from fastapi import FastAPI
from app.api.auth import router as auth_router

app = FastAPI(title="Skill Coach Hub API")
app.include_router(auth_router)

@app.get("/")
def health_check():
    return {"status": "ok"}

    