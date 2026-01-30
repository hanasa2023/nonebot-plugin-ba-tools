from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from nonebot.params import Depends
from nonebot_plugin_orm import AsyncSession, get_session

from nonebot_plugin_ba_tools.shared import get_subscribe_repository
from nonebot_plugin_ba_tools.shared.domain.repository.subscribe_repository import (
    SubscribeRepository,
)
from nonebot_plugin_ba_tools.shared.infra.reposirory.orm_subscribe_repository import (
    OrmSubscribeRepository,
)

from .application.student_data_synchronizer import (
    StudentDataSynchronizer,
)
from .application.student_information_use_case import (
    StudentInformationUseCase,
)
from .application.student_subscription_use_case import (
    StudentSubscriptionUseCase,
)
from .domain.port.student_data_gateway import (
    StudentDataGateway,
)
from .domain.repository.student_repository import (
    StudentRepository,
)
from .infra.repository.orm_student_repository import (
    OrmStudentRepository,
)
from .infra.service.schaledb_service import (
    SchaleDBService,
)

__all__ = [
    "get_schaledb_service",
    "get_student_data_synchronizer",
    "get_student_information_use_case",
    "get_student_repository",
    "get_student_subscription_use_case",
    "get_student_information_use_case_for_task",
    "get_student_repository_for_task",
    "get_subscribe_repository_for_task",
    "task_context",
]


async def get_student_repository(
    session: AsyncSession = Depends(get_session),
) -> StudentRepository:
    """获取学生仓库（Handler 专用）

    Args:
        session: 数据库会话，由 get_session 提供

    Returns:
        StudentRepository: 学生仓库实例
    """
    return OrmStudentRepository(session)


async def get_schaledb_service() -> StudentDataGateway:
    """获取 SchaleDB 学生数据网关

    Returns:
        StudentDataGateway: SchaleDB 学生数据网关实例
    """
    return SchaleDBService()


async def get_student_data_synchronizer(
    student_data_gateway: StudentDataGateway = Depends(get_schaledb_service),
    student_repository: StudentRepository = Depends(get_student_repository),
) -> StudentDataSynchronizer:
    """获取学生数据同步用例（Handler 专用）

    Args:
        student_data_gateway: 学生数据网关
        student_repository: 学生仓库

    Returns:
        StudentDataSynchronizer: 学生数据同步器
    """
    return StudentDataSynchronizer(student_data_gateway, student_repository)


async def get_student_subscription_use_case(
    subscribe_repository: SubscribeRepository = Depends(get_subscribe_repository),
) -> StudentSubscriptionUseCase:
    """获取学生订阅用例（Handler 专用）

    Args:
        subscribe_repository: 订阅仓库

    Returns:
        StudentSubscriptionUseCase: 学生订阅用例
    """
    return StudentSubscriptionUseCase(subscribe_repository)


async def get_student_information_use_case(
    student_repository: StudentRepository = Depends(get_student_repository),
) -> StudentInformationUseCase:
    """获取学生信息查询用例（Handler 专用）

    Args:
        student_repository: 学生仓库

    Returns:
        StudentInformationUseCase: 学生信息查询用例
    """
    return StudentInformationUseCase(student_repository)


def get_student_repository_for_task(
    session: AsyncSession,
) -> StudentRepository:
    """获取学生仓库（计划任务专用）

    用于计划任务和其他非 Handler 场景，需要手动传入 session。

    Args:
        session: 数据库会话

    Returns:
        StudentRepository: 学生仓库实例
    """
    return OrmStudentRepository(session)


def get_subscribe_repository_for_task(
    session: AsyncSession,
) -> SubscribeRepository:
    """获取订阅仓库（计划任务专用）

    用于计划任务和其他非 Handler 场景，需要手动传入 session。

    Args:
        session: 数据库会话

    Returns:
        SubscribeRepository: 订阅仓库实例
    """
    return OrmSubscribeRepository(session)


def get_student_information_use_case_for_task(
    session: AsyncSession,
) -> StudentInformationUseCase:
    """获取学生信息查询用例（计划任务专用）

    用于计划任务和其他非 Handler 场景。

    Args:
        session: 数据库会话

    Returns:
        StudentInformationUseCase: 学生信息查询用例
    """
    student_repository = get_student_repository_for_task(session)
    return StudentInformationUseCase(student_repository)


@asynccontextmanager
async def task_context() -> AsyncGenerator[dict[str, Any], None]:
    """为计划任务提供依赖注入上下文

    Usage:
        async with task_context() as ctx:
            # ctx 包含所有需要的用例和仓库
            await ctx['student_information_use_case'].get_birthday_students_today()

    Yields:
        dict: 包含以下键的字典：
            - 'student_repository': StudentRepository
            - 'subscribe_repository': SubscribeRepository
            - 'student_information_use_case': StudentInformationUseCase
            - 'student_subscription_use_case': StudentSubscriptionUseCase
            - 'session': AsyncSession (用于高级用途)
    """
    async with get_session() as session:
        # 构造所有需要的依赖
        student_repository = get_student_repository_for_task(session)
        subscribe_repository = get_subscribe_repository_for_task(session)
        student_information_use_case = StudentInformationUseCase(student_repository)
        student_subscription_use_case = StudentSubscriptionUseCase(subscribe_repository)

        # 返回依赖字典
        context = {
            "session": session,
            "student_repository": student_repository,
            "subscribe_repository": subscribe_repository,
            "student_information_use_case": student_information_use_case,
            "student_subscription_use_case": student_subscription_use_case,
        }

        yield context
