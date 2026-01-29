import re
from dataclasses import dataclass
from datetime import datetime

from .exception import (
    BirthdayParseError,
    ValidBirthdayError,
)


@dataclass(frozen=True)
class Birthday:
    """生日值对象

    表示一个人的生日，只包含月和日。
    由于生日是每年重复的事件，不需要存储年份。

    Attributes:
        month: 月份 (1-12)
        day: 日期 (1-31)
    """

    month: int
    """月份 (1-12)"""

    day: int
    """日期 (1-31)"""

    def __post_init__(self) -> None:
        """验证月和日的有效性"""
        if not (1 <= self.month <= 12):
            raise ValidBirthdayError("month", self.month)
        if not (1 <= self.day <= 31):
            raise ValidBirthdayError("day", self.day)

    def __str__(self) -> str:
        """返回格式化的生日字符串"""
        return f"{self.month}月{self.day}日"

    def __repr__(self) -> str:
        """返回详细的表示字符串"""
        return f"Birthday(month={self.month}, day={self.day})"

    def matches_today(self) -> bool:
        """检查今天是否是这个生日

        Returns:
            bool: 如果今天是这个生日则返回 True
        """
        today = datetime.now()
        return today.month == self.month and today.day == self.day

    def matches_date(self, month: int, day: int) -> bool:
        """检查指定的月日是否匹配这个生日

        Args:
            month: 月份
            day: 日期

        Returns:
            bool: 如果匹配则返回 True
        """
        return self.month == month and self.day == day

    def to_str(self) -> str:
        """返回格式化的生日字符串

        Args:
            format: 格式字符串，参考 datetime.strftime

        Returns:
            str: 格式化的生日字符串
        """
        return f"{self.month}月{self.day}日"

    @staticmethod
    def from_date_string(date_str: str) -> "Birthday":
        """从字符串解析生日

        支持的格式：
        - "3月12日" (中文格式)
        - "3/12" (斜杠格式)
        - "3-12" (连字符格式)

        Args:
            date_str: 日期字符串

        Returns:
            Birthday: 解析后的生日对象

        Raises:
            ValueError: 日期字符串格式不正确或日期无效
        """
        if not date_str:
            raise ValueError("日期字符串不能为空")

        pattern = r"^\s*(\d{1,2})\s*[月/-]\s*(\d{1,2})\s*[日]?\s*$"
        match = re.match(pattern, date_str)

        if not match:
            raise BirthdayParseError(
                date_str=date_str, details="支持格式：3月12日，3/12，3-12"
            )

        month_str, day_str = match.groups()
        month = int(month_str)
        day = int(day_str)
        return Birthday(month=month, day=day)

    @staticmethod
    def from_datetime(dt: datetime) -> "Birthday":
        """从 datetime 对象创建生日

        Args:
            dt: datetime 对象

        Returns:
            Birthday: 提取月和日的生日对象
        """
        return Birthday(month=dt.month, day=dt.day)
