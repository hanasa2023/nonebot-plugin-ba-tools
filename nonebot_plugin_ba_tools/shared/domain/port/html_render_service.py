from abc import ABC, abstractmethod


class HtmlRenderService(ABC):
    """HTML渲染服务"""

    @abstractmethod
    async def render_from_template(
        self,
        template_name: str,
        data: dict,
    ) -> bytes:
        """从模板渲染图片"""
        raise NotImplementedError
