from nonebot.params import Depends
from nonebot_plugin_orm import AsyncSession, get_session

from .domain.repository.subscribe_repository import SubscribeRepository
from .infra.reposirory.orm_subscribe_repository import OrmSubscribeRepository

__all__ = [
    "get_subscribe_repository",
]


async def get_subscribe_repository(
    session: AsyncSession = Depends(get_session),
) -> SubscribeRepository:
    """获取订阅仓库

    Args:
        session: 数据库会话，由 get_session 提供

    Returns:
        SubscribeRepository: 订阅仓库实例
    """
    return OrmSubscribeRepository(session)
