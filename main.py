from fastapi import FastAPI

from domain.auth.api import auth

app = FastAPI()
app.include_router(auth.router)

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}