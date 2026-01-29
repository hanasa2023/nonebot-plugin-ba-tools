from abc import ABC, abstractmethod

from typing_extensions import Self

from nonebot_plugin_ba_tools.features.student.domain.model.student import Student


class StudentDataGateway(ABC):
    """学生服务接口"""

    @abstractmethod
    async def __aenter__(self) -> Self:
        """异步上下文管理器入口"""
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """异步上下文管理器出口"""
        raise NotImplementedError

    @abstractmethod
    async def fetch_all_students(self) -> list[Student]:
        """获取学生信息"""
        raise NotImplementedError
