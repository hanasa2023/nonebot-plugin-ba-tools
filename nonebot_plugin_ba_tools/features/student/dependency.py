from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from nonebot.params import Depends
from nonebot_plugin_orm import AsyncSession, get_session

from nonebot_plugin_ba_tools.shared import get_subscribe_repository
from nonebot_plugin_ba_tools.shared.domain.port.html_render_service import (
    HtmlRenderService,
)
from nonebot_plugin_ba_tools.shared.domain.repository.subscribe_repository import (
    SubscribeRepository,
)
from nonebot_plugin_ba_tools.shared.infra.adapter.htmlkit_html_render_service import (
    HtmlkitHtmlRenderService,
)
from nonebot_plugin_ba_tools.shared.infra.reposirory.orm_subscribe_repository import (
    OrmSubscribeRepository,
)

from .application.student_birthday_use_case import (
    StudentBirthdayUseCase,
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


async def get_student_repository(
    session: AsyncSession = Depends(get_session),
) -> StudentRepository:
    return OrmStudentRepository(session)


async def get_schaledb_service() -> StudentDataGateway:
    return SchaleDBService()


async def get_html_render_service() -> HtmlRenderService:
    return HtmlkitHtmlRenderService()


async def get_student_data_synchronizer(
    student_data_gateway: StudentDataGateway = Depends(get_schaledb_service),
    student_repository: StudentRepository = Depends(get_student_repository),
) -> StudentDataSynchronizer:
    return StudentDataSynchronizer(student_data_gateway, student_repository)


async def get_student_subscription_use_case(
    subscribe_repository: SubscribeRepository = Depends(get_subscribe_repository),
) -> StudentSubscriptionUseCase:
    return StudentSubscriptionUseCase(subscribe_repository)


async def get_student_information_use_case(
    student_repository: StudentRepository = Depends(get_student_repository),
    html_render_service: HtmlRenderService = Depends(get_html_render_service),
) -> StudentInformationUseCase:
    return StudentInformationUseCase(
        student_repository,
        html_render_service,
    )


async def get_student_birthday_use_case(
    student_repository: StudentRepository = Depends(get_student_repository),
    html_render_service: HtmlRenderService = Depends(get_html_render_service),
) -> StudentBirthdayUseCase:
    return StudentBirthdayUseCase(
        student_repository,
        html_render_service,
    )


def get_student_repository_for_task(
    session: AsyncSession,
) -> StudentRepository:
    return OrmStudentRepository(session)


def get_subscribe_repository_for_task(
    session: AsyncSession,
) -> SubscribeRepository:
    return OrmSubscribeRepository(session)


def get_html_render_service_for_task() -> HtmlRenderService:
    return HtmlkitHtmlRenderService()


def get_student_birthday_use_case_for_task(
    session: AsyncSession,
) -> StudentBirthdayUseCase:
    student_repository = get_student_repository_for_task(session)
    html_render_service = get_html_render_service_for_task()
    return StudentBirthdayUseCase(student_repository, html_render_service)


@asynccontextmanager
async def task_context() -> AsyncGenerator[dict[str, Any], None]:
    async with get_session() as session:
        student_repository = get_student_repository_for_task(session)
        subscribe_repository = get_subscribe_repository_for_task(session)
        html_render_service = get_html_render_service_for_task()
        student_birthday_use_case = StudentBirthdayUseCase(
            student_repository,
            html_render_service,
        )
        student_subscription_use_case = StudentSubscriptionUseCase(subscribe_repository)

        context = {
            "session": session,
            "student_repository": student_repository,
            "subscribe_repository": subscribe_repository,
            "student_birthday_use_case": student_birthday_use_case,
            "student_subscription_use_case": student_subscription_use_case,
        }

        yield context
