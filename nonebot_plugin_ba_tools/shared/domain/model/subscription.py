from dataclasses import dataclass
from enum import Enum


class SubscriptionNotificationType(Enum):
    """可订阅的提醒类型"""

    BIRTHDAY = "birthday"
    """生日提醒"""
    BATTLE = "battle"
    """总力战/大决战提醒"""


@dataclass
class Subscription:
    """用户订阅模型"""

    id: int
    """订阅ID"""
    group_id: str
    """订阅的群组ID"""
    notification_type: SubscriptionNotificationType
    """订阅的功能类型"""
