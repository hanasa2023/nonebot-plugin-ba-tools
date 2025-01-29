from nonebot import on_regex, require
from nonebot.matcher import Matcher

require("nonebot_plugin_alconna")
from nonebot.adapters import Event
from nonebot.rule import to_me
from nonebot_plugin_alconna import (
    Args,
    Field,
    Match,
    Option,
    AlconnaMatcher,
    on_alconna,
    Alconna,
    Subcommand,
)

require("nonebot_plugin_uninfo")
from nonebot_plugin_uninfo import Uninfo

from ..config import plugin_config, config
from .client import Chat


def is_enable() -> bool:
    return plugin_config.chat_switch


if is_enable():
    c = Chat(
        api_key=plugin_config.openai_api_key,
        base_url=plugin_config.openai_base_url,
        preset_path=plugin_config.llm_path / "prompts.yaml",
        model=plugin_config.llm_model,
    )


chat: type[Matcher] = on_regex(
    rf"^[^{config.command_start}]([\s\S]+)",
    rule=to_me() & is_enable,
    priority=999,
)
chat_commands: type[AlconnaMatcher] = on_alconna(
    Alconna(
        "chat",
        Subcommand(
            "session",
            Option(
                "-c|--clear",
                dest="clear",
            ),
        ),
        Subcommand(
            "preset",
            Option(
                "-n|--new",
                Args[
                    "preset",
                    list[str],
                    Field(
                        completion=lambda: (
                            '请输入预设名称，及提示词（格式为: ["<your_preset_name>", "<your_prompt_content>"]）'
                        )
                    ),
                ],
                dest="new",
            ),
            Option(
                "-c|--change",
                Args["preset", str, Field(completion=lambda: "请输入要更换的预设名称")],
                dest="change",
            ),
            Option(
                "-r|--reset",
                dest="reset",
            ),
            Option("-l|--list", dest="list"),
        ),
    ),
    use_cmd_start=True,
    block=True,
)


@chat.handle()
async def _(event: Event, session: Uninfo) -> None:
    resp = await c.chat(session.id, event.get_plaintext())
    await chat.finish(resp)


@chat_commands.assign("session.clear")
async def _(session: Uninfo) -> None:
    msg = c.clear_session(session.id)
    await chat_commands.finish(msg)


@chat_commands.assign("preset.new")
async def _(preset: Match[list[str]]) -> None:
    msg = await c.create_new_prompt(preset.result[0], preset.result[1])
    await chat_commands.finish(msg)


@chat_commands.assign("preset.change")
async def _(preset: Match[str]) -> None:
    msg = c.change_preset(preset.result)
    await chat_commands.finish(msg)


@chat_commands.assign("preset.reset")
async def _() -> None:
    msg = c.reset_preset()
    await chat_commands.finish(msg)


@chat_commands.assign("preset.list")
async def _() -> None:
    presets: list[str] = c.presets
    msg: str = "可用的预设有：\n"
    for preset in presets:
        msg += f"- {preset}\n"
    await chat_commands.finish(msg)
