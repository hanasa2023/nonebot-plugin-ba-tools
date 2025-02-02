from __future__ import annotations

from nonebot import logger, on_regex, require
from nonebot.matcher import Matcher

require("nonebot_plugin_alconna")
from nonebot.adapters import Event
from nonebot.rule import to_me
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatcher,
    Args,
    Field,
    Match,
    Option,
    Subcommand,
    UniMessage,
    on_alconna,
)

require("nonebot_plugin_uninfo")
from nonebot_plugin_uninfo import SceneType, Uninfo

from ..config import LLM_DIR, ConfigManager, config
from ..utils.user_info import is_superuser
from .client import Chat


def is_enable() -> bool:
    return ConfigManager.get().chat.enable


def init_chat() -> Chat | None:
    if not ConfigManager.get().chat.enable:
        return None
    try:
        models = ConfigManager.get().chat.models
        model = next(model for model in models if model.name == ConfigManager.get().chat.current_model)
        return Chat(
            api_key=model.api_key,
            base_url=model.base_url,
            model=model.name,
            preset_path=LLM_DIR / "prompts.yaml",
        )
    except StopIteration:
        logger.error("未找到指定的模型")
        return None


chat: type[Matcher] = on_regex(
    rf"^[^{''.join(config.command_start)}]([\s\S]+)",
    rule=to_me() & is_enable,
    priority=999,
)
chat_commands: type[AlconnaMatcher] = on_alconna(
    Alconna(
        "bachat",
        Subcommand(
            "session",
            Option(
                "-c|--clear",
                dest="clear",
                help_text="清除当前会话",
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
                help_text="新建预设",
            ),
            Option(
                "-c|--change",
                Args["preset", str, Field(completion=lambda: "请输入要更换的预设名称")],
                dest="change",
                help_text="更换预设",
            ),
            Option(
                "-r|--reset",
                dest="reset",
                help_text="重置预设",
            ),
            Option(
                "-l|--list",
                dest="list",
                help_text="列出所有预设",
            ),
        ),
        # Option(
        #     "-b|--balance",
        #     dest="balance",
        #     help_text="查看余额",
        # ),
        Subcommand(
            "mode",
            Option(
                "-t|--toggle",
                dest="toggle",
                help_text="切换回复模式为文本/图片",
            ),
        ),
        Option(
            "-e|--enable",
            dest="enable",
            help_text="启用聊天功能",
        ),
        Option(
            "-d|--disable",
            dest="disable",
            help_text="禁用聊天功能",
        ),
        Option(
            "-t|--toggle",
            dest="toggle",
            help_text="切换聊天功能状态",
        ),
    ),
    use_cmd_start=True,
    block=True,
)


@chat.handle()
async def _(event: Event, session: Uninfo) -> None:
    c: Chat | None = init_chat()
    if not c:
        await chat.finish("未启用聊天功能")
    resp = await c.chat(session.id, event.get_plaintext())
    if ConfigManager.get().chat.reply_mode == "text":
        await chat.finish(resp)
    else:
        from ..utils.addition_for_htmlrender import md_to_pic

        pic: bytes = await md_to_pic(resp if resp else "未收到回复")
        msg = UniMessage.image(raw=pic)
        await msg.send()
        await chat.finish()


@chat_commands.assign("session.clear")
async def _(session: Uninfo) -> None:
    c: Chat | None = init_chat()
    if not c:
        await chat.finish("未启用聊天功能")
    msg = c.clear_session(session.id)
    await chat_commands.finish(msg)


@chat_commands.assign("preset.new")
async def _(preset: Match[list[str]]) -> None:
    c: Chat | None = init_chat()
    if not c:
        await chat.finish("未启用聊天功能")
    msg = await c.create_new_prompt(preset.result[0], preset.result[1])
    await chat_commands.finish(msg)


@chat_commands.assign("preset.change")
async def _(preset: Match[str], session: Uninfo) -> None:
    c: Chat | None = init_chat()
    if not c:
        await chat.finish("未启用聊天功能")
    if session.scene.type == SceneType.GROUP:
        logger.info(f"session: {session.scene.id}")
        is_group_owner = session.member and session.member.role and session.member.role.id == "OWNER"
        is_group_admin = session.member and session.member.role and session.member.role.id == "ADMINISTRATOR"
        if is_group_owner or is_group_admin or is_superuser(session.user.id):
            msg = c.change_preset(preset.result)
            await chat_commands.finish(msg)

        else:
            await chat_commands.finish("只有群主和(超级)管理员可以更改预设")
    elif session.scene.type == SceneType.PRIVATE:
        if is_superuser(session.user.id):
            msg = c.change_preset(preset.result)
            await chat_commands.finish(msg)
        else:
            await chat_commands.finish("只有超级用户可以更改预设")


@chat_commands.assign("preset.reset")
async def _(session: Uninfo) -> None:
    c: Chat | None = init_chat()
    if not c:
        await chat.finish("未启用聊天功能")
    if session.scene.type == SceneType.GROUP:
        logger.info(f"session: {session.scene.id}")
        is_group_owner = session.member and session.member.role and session.member.role.id == "OWNER"
        is_group_admin = session.member and session.member.role and session.member.role.id == "ADMINISTRATOR"
        if is_group_owner or is_group_admin or is_superuser(session.user.id):
            msg = c.reset_preset()
            await chat_commands.finish(msg)

        else:
            await chat_commands.finish("只有群主和(超级)管理员可以重置预设")
    elif session.scene.type == SceneType.PRIVATE:
        if is_superuser(session.user.id):
            msg = c.reset_preset()
            await chat_commands.finish(msg)
        else:
            await chat_commands.finish("只有超级用户可以更改预设")


@chat_commands.assign("preset.list")
async def _() -> None:
    c: Chat | None = init_chat()
    if not c:
        await chat.finish("未启用聊天功能")
    presets: list[str] = c.presets
    msg: str = "可用的预设有：\n"
    for preset in presets:
        msg += f"- {preset}\n"
    await chat_commands.finish(msg)


@chat_commands.assign("mode.toggle")
async def _(session: Uninfo) -> None:
    if session.scene.type == SceneType.GROUP:
        is_group_owner = session.member and session.member.role and session.member.role.id == "OWNER"
        is_group_admin = session.member and session.member.role and session.member.role.id == "ADMINISTRATOR"
        if is_group_owner or is_group_admin or is_superuser(session.user.id):
            cfg = ConfigManager.get()
            cfg.chat.reply_mode = "text" if cfg.chat.reply_mode == "image" else "image"
            ConfigManager.set(cfg)
            await chat_commands.finish(f"已切换回复模式为{cfg.chat.reply_mode}")
        else:
            await chat_commands.finish("只有群主和(超级)管理员可以切换回复模式")
    elif session.scene.type == SceneType.PRIVATE:
        if is_superuser(session.user.id):
            cfg = ConfigManager.get()
            cfg.chat.reply_mode = "text" if cfg.chat.reply_mode == "image" else "image"
            ConfigManager.set(cfg)
            await chat_commands.finish(f"已切换回复模式为{cfg.chat.reply_mode}")
        else:
            await chat_commands.finish("只有超级用户可以切换回复模式")


@chat_commands.assign("enable")
async def _(session: Uninfo) -> None:
    if session.scene.type == SceneType.PRIVATE:
        if is_superuser(session.user.id):
            cfg = ConfigManager.get()
            cfg.chat.enable = True
            ConfigManager.set(cfg)
            await chat_commands.finish("已启用聊天功能")
        else:
            await chat_commands.finish("只有超级用户可以启用聊天功能")
    elif session.scene.type == SceneType.GROUP:
        is_group_owner = session.member and session.member.role and session.member.role.id == "OWNER"
        is_group_admin = session.member and session.member.role and session.member.role.id == "ADMINISTRATOR"
        if is_group_owner or is_group_admin or is_superuser(session.user.id):
            cfg = ConfigManager.get()
            cfg.chat.enable = True
            ConfigManager.set(cfg)
            await chat_commands.finish("已启用聊天功能")
        else:
            await chat_commands.finish("只有群主和(超级)管理员可以启用聊天功能")


@chat_commands.assign("disable")
async def _(session: Uninfo) -> None:
    if session.scene.type == SceneType.PRIVATE:
        if is_superuser(session.user.id):
            cfg = ConfigManager.get()
            cfg.chat.enable = False
            ConfigManager.set(cfg)
            await chat_commands.finish("已禁用聊天功能")
        else:
            await chat_commands.finish("只有超级用户可以禁用聊天功能")
    elif session.scene.type == SceneType.GROUP:
        is_group_owner = session.member and session.member.role and session.member.role.id == "OWNER"
        is_group_admin = session.member and session.member.role and session.member.role.id == "ADMINISTRATOR"
        if is_group_owner or is_group_admin or is_superuser(session.user.id):
            cfg = ConfigManager.get()
            cfg.chat.enable = False
            ConfigManager.set(cfg)
            await chat_commands.finish("已禁用聊天功能")
        else:
            await chat_commands.finish("只有群主和(超级)管理员可以禁用聊天功能")


@chat_commands.assign("toggle")
async def _(session: Uninfo) -> None:
    if session.scene.type == SceneType.PRIVATE:
        if is_superuser(session.user.id):
            cfg = ConfigManager.get()
            cfg.chat.enable = not cfg.chat.enable
            ConfigManager.set(cfg)
            await chat_commands.finish(f"已{'启用' if ConfigManager.get().chat.enable else '禁用'}聊天功能")
        else:
            await chat_commands.finish("只有超级用户可以切换聊天功能状态")

    elif session.scene.type == SceneType.GROUP:
        is_group_owner = session.member and session.member.role and session.member.role.id == "OWNER"
        is_group_admin = session.member and session.member.role and session.member.role.id == "ADMINISTRATOR"
        if is_group_owner or is_group_admin or is_superuser(session.user.id):
            cfg = ConfigManager.get()
            cfg.chat.enable = not cfg.chat.enable
            ConfigManager.set(cfg)
            await chat_commands.finish(f"已{'启用' if ConfigManager.get().chat.enable else '禁用'}聊天功能")
        else:
            await chat_commands.finish("只有群主和(超级)管理员可以切换聊天功能状态")
