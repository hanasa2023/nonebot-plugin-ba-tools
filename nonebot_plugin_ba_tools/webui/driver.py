from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nonebot import get_driver
from nonebot.drivers import ReverseDriver
from nonebot.drivers.fastapi import Driver as FastAPIDriver


driver: FastAPIDriver = get_driver()  # type: ignore

if not isinstance(driver, ReverseDriver) or not isinstance(driver, FastAPI):
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
