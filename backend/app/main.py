from fastapi import FastAPI

app = FastAPI(title="Skill Coach Hub API")

@app.get("/")
def health_check():
    return {"status": "ok"}

    