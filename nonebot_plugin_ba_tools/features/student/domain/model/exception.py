from typing import Literal


class BirthdayParseError(ValueError):
    """当生日字符串格式不正确或日期不存在时抛出"""

    def __init__(self, date_str: str, details: str = "") -> None:
        msg = f"无法识别生日格式: '{date_str}'"
        if details:
            msg += f" ({details})"
        super().__init__(msg)


class ValidBirthdayError(ValueError):
    """当生日日期范围错误时抛出"""

    def __init__(self, err_type: Literal["month", "day"], receive: int) -> None:
        if err_type == "month":
            msg = f"月份必须在 1-12 之间，收到: {receive}"
        else:
            msg = f"日期必须在 1-31 之间，收到: {receive}"
        super().__init__(msg)
