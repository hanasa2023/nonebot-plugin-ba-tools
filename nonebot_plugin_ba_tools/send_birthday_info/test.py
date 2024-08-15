from nonebot import on_command

test = on_command("test")


@test.handle()
async def _():
    await test.finish("ok")
