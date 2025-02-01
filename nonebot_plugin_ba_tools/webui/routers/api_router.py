import time

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from loguru import logger
from nonebot.compat import PYDANTIC_V2, model_dump, type_validate_python
from pydantic import ValidationError

from ...utils.get_info import get_all_info

from ...config import Config, ConfigManager
from ..utils import verify_token

api_router = APIRouter(
    prefix="/api",
)


@api_router.post("/login")
async def login(data: HTTPBasicCredentials):
    config = ConfigManager.get()
    if data.username != config.webui.username and data.password != config.webui.password:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = jwt.encode(
        {
            "username": data.username,
            "timestamp": time.time() + 24 * 60 * 60,
        },
        config.webui.api_access_token,
        algorithm="HS256",
    )
    return {"token": token}


@api_router.get(
    "/getConfig",
    dependencies=[Depends(verify_token)],
)
def get_config() -> Config:
    return ConfigManager.get()


@api_router.get(
    "/getConfigSchema",
    dependencies=[Depends(verify_token)],
)
def get_config_schema() -> dict:
    if PYDANTIC_V2:
        return Config.model_json_schema()
    else:
        return Config.schema()


@api_router.post(
    "/setConfig",
    dependencies=[Depends(verify_token)],
)
async def set_config(cfg: Config):
    try:
        new_cfg: Config = type_validate_python(
            Config,
            model_dump(
                cfg,
            ),
        )
        old_cfg: Config = ConfigManager.get()
    except ValidationError as e:
        logger.debug(cfg)
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.json(),
        ) from e

    try:
        ConfigManager.set(new_cfg)
        return {"message": "配置更新成功"}
    except Exception as e:
        logger.exception("设置新配置失败，回滚至原配置")
        ConfigManager.set(old_cfg)
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@api_router.get("/resetConfig", dependencies=[Depends(verify_token)])
def reset_config():
    ConfigManager.reset()
    return {"message": "Config reset successfully."}


@api_router.get("/getInfo", dependencies=[Depends(verify_token)])
def get_info():
    try:
        return get_all_info()
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
