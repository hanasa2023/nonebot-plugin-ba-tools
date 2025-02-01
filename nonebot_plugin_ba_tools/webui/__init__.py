from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.staticfiles import StaticFiles

from .driver import app
from .routers import api_router, webui_router

router = APIRouter()


router.include_router(webui_router)
router.include_router(api_router)

app.include_router(
    router,
    prefix="/batools",
    dependencies=[],
)


app.mount(
    "/batools",
    StaticFiles(directory=Path(__file__).parent / "static"),
)
