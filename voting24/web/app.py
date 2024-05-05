from fastapi import FastAPI

from .routes import game

app = FastAPI(
    title="Voting app 2024",
    version="0.0.1",
)

app.include_router(game.router)
