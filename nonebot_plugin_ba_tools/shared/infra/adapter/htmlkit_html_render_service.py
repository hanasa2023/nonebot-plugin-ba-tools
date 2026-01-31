from pathlib import Path

from nonebot_plugin_htmlkit import template_to_pic

from nonebot_plugin_ba_tools.shared.domain.port.html_render_service import (
    HtmlRenderService,
)


class HtmlkitHtmlRenderService(HtmlRenderService):
    """HTML渲染服务"""

    def __init__(self, template_path: Path | None = None) -> None:
        self.template_dir = (
            template_path if template_path else (Path(__file__).parents[1] / "template")
        )

    async def render_from_template(
        self,
        template_name: str,
        data: dict,
    ) -> bytes:
        """从模板渲染图片"""

        return await template_to_pic(
            template_path=self.template_dir,
            template_name=template_name,
            templates=data,
            dpi=120,
            max_width=1000,
            device_height=1200,
            allow_refit=True,
        )
