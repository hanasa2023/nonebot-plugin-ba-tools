from datetime import datetime

import pytest
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.adapters.onebot.v11.event import Sender
from nonebug import App


def make_event(msg: str = "") -> GroupMessageEvent:
    return GroupMessageEvent(
        time=int(datetime.now().timestamp()),
        self_id=123345,
        post_type="message",
        sub_type="normal",
        user_id=45678,
        message_type="group",
        message_id=41414,
        message=Message(msg),
        original_message=Message(msg),
        raw_message=msg,
        font=1,
        sender=Sender(user_id=45678),
        group_id=23456,
    )


@pytest.mark.asyncio
async def test_switch(app: App):
    from nonebot_plugin_ba_tools.send_birthday_info.command import birthday_info_switch

    async with app.test_matcher(birthday_info_switch) as ctx:
        bot = ctx.create_bot()
        event = make_event("/ba学生生日订阅 开启")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "权限不足", bot=bot)
        ctx.should_finished(birthday_info_switch)
