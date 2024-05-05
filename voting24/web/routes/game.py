from typing import Annotated

from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from voting24.db.database import Database
from voting24.game.game import Key
from voting24.web.dependencies import TemplateResponse, get_database, template

router = APIRouter()


@router.get("/game/{key}")
def get_game(
    key: Key,
    template: Annotated[TemplateResponse, Depends(template)],
    database: Annotated[Database, Depends(get_database)],
) -> HTMLResponse:
    return template("game.html", {"game": database.load_game(key)})
