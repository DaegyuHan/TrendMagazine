from fastapi import FastAPI

from domain.article.api import article
from domain.auth.api import auth
from domain.user.api import user

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(article.router)

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}