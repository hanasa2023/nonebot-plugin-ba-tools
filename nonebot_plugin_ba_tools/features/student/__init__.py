from nonebot import get_driver, logger
from nonebot_plugin_orm import get_session

from .application import StudentDataSynchronizer
from .handler.get_student_birthday import birthday_matcher
from .handler.student_info_subcriber import send_birthday_info
from .handler.subscribe_student_birthday import birthday_subscriber
from .handler.update_student_info import update_student_info_matcher
from .infra.repository.orm_student_repository import OrmStudentRepository
from .infra.service.schaledb_service import SchaleDBService
from .infra.table.students import Students

__all__ = [
    "Students",
    "birthday_matcher",
    "birthday_subscriber",
    "send_birthday_info",
    "update_student_info_matcher",
]

driver = get_driver()


@driver.on_startup
async def makesure_student_table_exists() -> None:
    """启动时检查并同步学生数据表"""
    try:
        async with get_session() as session:
            student_repository = OrmStudentRepository(session)
            student_data_gateway = SchaleDBService()
            synchronizer = StudentDataSynchronizer(
                student_data_gateway, student_repository
            )

            # 执行同步检查
            await synchronizer.check_synchronization()
    except Exception as e:
        logger.error(f"启动时同步学生数据失败: {e}", exc_info=True)
