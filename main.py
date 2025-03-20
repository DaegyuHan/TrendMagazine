from fastapi import FastAPI

from domain.auth.api import auth
from domain.user.api import user

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}