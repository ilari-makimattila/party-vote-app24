import subprocess  # noqa: S404
from pathlib import Path
from typing import Annotated

from fastapi import HTTPException, Response
from fastapi.routing import APIRouter
from pydantic import Field

_ui_path = Path(__file__).parent.parent.parent / "ui"


def _render(file_path: Path) -> str:
    if not (_ui_path / file_path).exists():
        raise HTTPException(status_code=404)

    result = subprocess.run(
        [  # noqa: S603  # it's not untrusted content
            "/usr/bin/npx",
            "sass",
            "--no-source-map",
            str(file_path),
        ],
        capture_output=True,
        text=True,
        cwd=str(_ui_path),
        check=True,
    )
    return result.stdout


style_router = APIRouter(
    prefix="/css",
)


@style_router.get("/{css_file:path}.css")
def serve_css(css_file: Annotated[str, Field(pattern=r"^[\w-]+$")]) -> Response:
    file_path = Path("styles") / (css_file + ".scss")

    content = _render(file_path)
    return Response(
        content,
        media_type="text/css",
    )
