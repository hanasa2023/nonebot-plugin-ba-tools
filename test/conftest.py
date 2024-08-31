import os

import nonebot
import pytest
from nonebot.adapters.onebot.v11 import Adapter
from nonebug import NONEBOT_INIT_KWARGS

os.environ["ENVIRONMENT"] = "test"


@pytest.fixture(scope="session", autouse=True)
def load_bot():
    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)

    nonebot.load_from_toml("pyproject.toml")


def pytest_configure(config: pytest.Config):
    config.stash[NONEBOT_INIT_KWARGS] = {"command_start": {"/"}, "log_level": "DEBUG"}
