from nonebot_plugin_orm import Model
from sqlalchemy.orm import Mapped, mapped_column

from nonebot_plugin_ba_tools.shared.domain.model.subscription import (
    SubscriptionNotificationType,
)


class Subscriptions(Model):
    """用户功能订阅表"""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[str]
    notification_type: Mapped[SubscriptionNotificationType]
