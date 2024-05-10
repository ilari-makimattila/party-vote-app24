import logging
import subprocess  # noqa: S404
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

from fastapi import HTTPException, Response
from fastapi.routing import APIRouter
from pydantic import Field

_ui_path = Path(__file__).parent.parent.parent / "ui"


@dataclass
class _CacheItem:
    modified: float
    output: str


_rendering_cache: dict[Path, _CacheItem] = {}


def _render(file_path: Path) -> str:
    if not (_ui_path / file_path).exists():
        raise HTTPException(status_code=404)

    modified = (_ui_path / file_path).stat().st_mtime
    output = None
    if file_path not in _rendering_cache or _rendering_cache[file_path].modified < modified:
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
            check=False,
        )
        if result.returncode != 0:
            logging.error("sass error: %s", result.stderr)
            raise HTTPException(status_code=500, detail=result.stderr)
        output = result.stdout
        _rendering_cache[file_path] = _CacheItem(modified, output)
    else:
        output = _rendering_cache[file_path].output
    return output


script_router = APIRouter(
    prefix="/js",
)

style_router = APIRouter(
    prefix="/css",
)


@script_router.get("/npm/{script_file:path}.js")
def serve_npm_script(script_file: Annotated[str, Field(pattern=r"^[\w\-]+((\.|/)([\w\-]+))*$")]) -> Response:
    file_path = Path("node_modules") / (script_file + ".js")
    full_path = _ui_path / file_path
    if not full_path.is_absolute() or not full_path.exists():
        raise HTTPException(status_code=404)
    return Response(
        (_ui_path / file_path).read_text(),
        media_type="text/javascript",
    )


@style_router.get("/{css_file:path}.css")
def serve_css(css_file: Annotated[str, Field(pattern=r"^[\w-]+$")]) -> Response:
    file_path = Path("styles") / (css_file + ".scss")

    content = _render(file_path)
    return Response(
        content,
        media_type="text/css",
    )
