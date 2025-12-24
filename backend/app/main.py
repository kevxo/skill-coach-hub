from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.routes.user import router as user_router
from app.api.routes.coach import router as coach_router

app = FastAPI(title="Skill Coach Hub API")
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(coach_router)

@app.get("/")
def health_check():
    return {"status": "ok"}

    