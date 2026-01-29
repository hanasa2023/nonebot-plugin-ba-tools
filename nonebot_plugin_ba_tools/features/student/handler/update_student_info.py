from nonebot import logger
from nonebot.params import Depends
from nonebot_plugin_alconna import Alconna, AlconnaMatcher, on_alconna

from nonebot_plugin_ba_tools.features.student.application import (
    StudentDataSynchronizer,
)
from nonebot_plugin_ba_tools.features.student.dependency import (
    get_student_data_synchronizer,
)

# 命令定义
_update_student_info = Alconna("更新BA学生数据")

update_student_info_matcher: type[AlconnaMatcher] = on_alconna(
    _update_student_info,
    use_cmd_start=True,
)


@update_student_info_matcher.handle()
async def _(
    synchronizer: StudentDataSynchronizer = Depends(get_student_data_synchronizer),
) -> None:
    try:
        await update_student_info_matcher.send("正在从 SchaleDB 获取学生数据...")
        message = await synchronizer.synchronize()

    except Exception as e:
        error_msg = f"❌ 学生数据更新失败: {e!s}"
        logger.error(f"处理更新学生数据命令异常: {e}", exc_info=True)
        await update_student_info_matcher.finish(error_msg)

    await update_student_info_matcher.finish(message)
