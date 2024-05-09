import logging
from collections.abc import Mapping
from typing import Any, Protocol

from fastapi import BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

from voting24.db.database import Database
from voting24.db.hardcoded_eurovision24_game import hardcoded_datatabase

_templates = Jinja2Templates(directory="voting24/web/templates")


class TemplateResponse(Protocol):
    def __call__(  # noqa: PLR0913, PLR0917
        self,
        template: str,
        context: dict[str, Any],
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTasks | None = None,
     ) -> HTMLResponse:
        ...


def get_database() -> Database:
    return hardcoded_datatabase


def template(request: Request) -> TemplateResponse:
    def respond(  # noqa: PLR0913, PLR0917
        template: str,
        context: dict[str, Any] | None = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> HTMLResponse:
        new_context = {"request": request} | (context or {})
        try:
            return _templates.TemplateResponse(
                request,
                template,
                new_context,
                status_code,
                headers,
                media_type,
                background,
            )
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception("Unable to render template", extra={"template": template, "context": context, "error": e})
            err_context = {
                "request": request,
                "error": e,
                "context": context,
                "stacktrace": "",
                "source": "rendering template",
            }
            return _templates.TemplateResponse(request, "error500.html", err_context, status_code=500)

    return respond
