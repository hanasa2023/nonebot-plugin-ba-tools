from nonebot.params import Depends
from nonebot_plugin_orm import AsyncSession, get_session

from nonebot_plugin_ba_tools.shared import get_subscribe_repository
from nonebot_plugin_ba_tools.shared.domain.repository.subscribe_repository import (
    SubscribeRepository,
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
]


async def get_student_repository(
    session: AsyncSession = Depends(get_session),
) -> StudentRepository:
    """获取学生仓库

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
    """获取学生数据同步用例

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
    """获取学生订阅用例

    Args:
        subscribe_repository: 订阅仓库

    Returns:
        StudentSubscriptionUseCase: 学生订阅用例
    """
    return StudentSubscriptionUseCase(subscribe_repository)


async def get_student_information_use_case(
    student_repository: StudentRepository = Depends(get_student_repository),
) -> StudentInformationUseCase:
    """获取学生信息查询用例

    Args:
        student_repository: 学生仓库

    Returns:
        StudentInformationUseCase: 学生信息查询用例
    """
    return StudentInformationUseCase(student_repository)
