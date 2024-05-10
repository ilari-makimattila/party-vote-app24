from typing import Annotated

from fastapi import Cookie, Depends, Form, Header, HTTPException, Response
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from voting24.db.database import ChoiceNotFoundError, Database, GameNotFoundError, VoteItemNotFoundError
from voting24.game.game import Game, Key, Name
from voting24.web.dependencies import TemplateResponse, get_database, template

router = APIRouter(
    prefix="/game/{key}",
)


def get_game(
    key: Key,
    database: Annotated[Database, Depends(get_database)],
) -> Game:
    try:
        return database.load_game(key)
    except GameNotFoundError:
        raise HTTPException(status_code=404, detail=f"Game {key} not found") from None


def get_player(
    key: Key,
    player_name: Annotated[Name | None, Cookie()] = None,
) -> str:
    if not player_name:
        raise HTTPException(status_code=303, headers={"Location": f"/game/{key}"})
    return player_name


@router.get("/item")
def forward_to_unvoted(
    key: Key,
    game: Annotated[Game, Depends(get_game)],
    player_name: Annotated[Name, Depends(get_player)],
) -> Response:
    if not player_name:
        return RedirectResponse(f"/game/{key}", status_code=303)
    if player_name not in (player.name for player in game.players):
        return RedirectResponse(f"/game/{key}", status_code=303)

    return RedirectResponse(f"/game/{key}/item/{game.next_unvoted_item(player_name)}", status_code=303)


@router.get("/item/{item_key}")
def play_item(
    game: Annotated[Game, Depends(get_game)],
    player_name: Annotated[Name, Depends(get_player)],
    template: Annotated[TemplateResponse, Depends(template)],
    key: Key,
    item_key: Key,
) -> Response:
    if player_name not in (player.name for player in game.players):
        return RedirectResponse(f"/game/{key}", status_code=303)

    item = next((item for item in game.items if item.key == item_key), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_key} not found")

    return template(
        "game_item.html",
        {
            "game": game,
            "item": item,
            "player_name": player_name,
            "player": next((player for player in game.players if player.name == player_name), None),
            "is_last_item": game.items.index(item) == len(game.items) - 1,
        },
    )


@router.post("/item/{item_key}")
def vote_item(  # noqa: PLR0913, PLR0917
    game: Annotated[Game, Depends(get_game)],
    database: Annotated[Database, Depends(get_database)],
    template: Annotated[TemplateResponse, Depends(template)],
    player_name: Annotated[Name, Depends(get_player)],
    item_key: Key,
    vote: Annotated[Key | None, Form()] = None,
    hx_request: Annotated[bool, Header()] = False,  # noqa: FBT002  # allow boolean args in routes
) -> Response:
    player = game.player(player_name)
    if player is None:
        if hx_request:
            raise HTTPException(status_code=404, detail=f"Player {player_name} not found in game {game.name}")
        return RedirectResponse(f"/game/{game.key}", status_code=303)

    item = next((item for item in game.items if item.key == item_key), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_key} not found in game {game.name}")

    all_ok = vote is not None
    try:
        if vote:
            database.vote(player_name, game.key, item_key, vote)
    except (VoteItemNotFoundError, ChoiceNotFoundError):
        all_ok = False

    if not all_ok or hx_request:
        if hx_request:
            game_item_index = game.items.index(item)
            if game_item_index < len(game.items) - 1:
                item = game.items[game_item_index + 1]

        template_file = "partials/game_item.html" if hx_request else "game_item.html"
        return template(
            template_file,
            {
                "game": game,
                "item": item,
                "player_name": player_name,
                "player": player,
                "is_last_item": game.items.index(item) == len(game.items) - 1,
            },
            status_code=200 if all_ok else 400,
            headers={"hx-push-url": f"/game/{game.key}/item/{item.key}"} if hx_request else None,
        )

    next_unvoted_item = game.next_unvoted_item(player_name)
    if not next_unvoted_item:
        return RedirectResponse(f"/game/{game.key}/results", status_code=303)
    return RedirectResponse(f"/game/{game.key}/item/{next_unvoted_item}", status_code=303)
