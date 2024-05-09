from fastapi import FastAPI

from .routes import game, play
from .ui import script_router, style_router

app = FastAPI(
    title="Voting app 2024",
    version="0.0.1",
)

app.include_router(style_router)
app.include_router(script_router)
app.include_router(game.router)
app.include_router(play.router)
