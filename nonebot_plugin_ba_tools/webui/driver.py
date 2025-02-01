from fastapi.middleware.cors import CORSMiddleware
from nonebot import get_driver
from nonebot.drivers.fastapi import Driver as FastAPIDriver

driver = get_driver()

if not isinstance(driver, FastAPIDriver):
    raise NotImplementedError("This plugin only supports FastAPI driver.")

app = driver.server_app

app.separate_input_output_schemas = False
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
