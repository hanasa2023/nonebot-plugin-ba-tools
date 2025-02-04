from fastapi.middleware.cors import CORSMiddleware
from nonebot import get_driver
from nonebot.drivers.fastapi import Driver as FastAPIDriver

from ..config import ConfigManager

driver = get_driver()

if ConfigManager.get().webui.enable:
    if not isinstance(driver, FastAPIDriver):
        raise NotImplementedError("This feature only support FastAPI driver.")

    app = driver.server_app

    app.separate_input_output_schemas = False
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
