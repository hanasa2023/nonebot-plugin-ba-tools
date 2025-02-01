from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

webui_router = APIRouter(prefix="/webui")

templates = Jinja2Templates(directory=Path(__file__).parents[1] / "templates")


@webui_router.get("", response_class=HTMLResponse)
async def index(request: Request):
    #     if "token" not in request.cookies:
    #         return RedirectResponse("/batools/webui/login")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "BA Tools WebUI",
            "description": "NoneBot Plugin BA Tools WebUI",
        },
    )
