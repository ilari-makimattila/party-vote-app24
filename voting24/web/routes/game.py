from typing import Annotated

from fastapi import Depends, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter

from voting24.db.database import Database, GameNotFoundError, PlayerAlreadyExistsError
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


@router.post("/game/{key}/join")
def join_game(
    database: Annotated[Database, Depends(get_database)],
    template: Annotated[TemplateResponse, Depends(template)],
    key: Key,
    player_name: Annotated[str, Form()],
    force: Annotated[int, Form()] = 0,
) -> Response:
    try:
        database.join_game(key, player_name, join_as_existing=force == 1)
    except PlayerAlreadyExistsError:
        return template(
            "game.html",
            {
                "game": database.load_game(key),
                "join": {
                    "player_name": player_name,
                    "player_exists": True,
                },
            },
            status_code=400,
        )
    except GameNotFoundError:
        return Response(status_code=404, content=f"Game {key} not found")

    response = RedirectResponse(f"/game/{key}/item", status_code=303)
    response.set_cookie("player_name", player_name, httponly=True)
    return response


@router.get("/game/{key}/results")
def get_results(
    database: Annotated[Database, Depends(get_database)],
    template: Annotated[TemplateResponse, Depends(template)],
    key: Key,
) -> Response:
    try:
        return template("game_results.html", {"game": database.load_game(key)})
    except GameNotFoundError:
        return Response(status_code=404, content=f"Game {key} not found")
