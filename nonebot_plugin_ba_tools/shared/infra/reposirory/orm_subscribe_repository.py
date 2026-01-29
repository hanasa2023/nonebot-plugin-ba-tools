from nonebot_plugin_orm import AsyncSession
from sqlalchemy.sql import delete, select

from nonebot_plugin_ba_tools.shared.domain.model.subscription import (
    Subscription,
    SubscriptionNotificationType,
)
from nonebot_plugin_ba_tools.shared.domain.repository.subscribe_repository import (
    SubscribeRepository,
)
from nonebot_plugin_ba_tools.shared.infra.table.subscriptions import Subscriptions


class OrmSubscribeRepository(SubscribeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_subscribe(
        self, group_id: str, notification_type: SubscriptionNotificationType
    ) -> None:
        sub = Subscriptions(group_id=group_id, notification_type=notification_type)
        self.session.add(sub)
        await self.session.commit()

    async def remove_subscribe(
        self, group_id: str, notification_type: SubscriptionNotificationType
    ) -> None:
        stmt = delete(Subscriptions).where(
            Subscriptions.group_id == group_id,
            Subscriptions.notification_type == notification_type,
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_subscribed_groups(
        self, notification_type: SubscriptionNotificationType
    ) -> list[Subscription]:
        stmt = select(Subscriptions).where(
            Subscriptions.notification_type == notification_type
        )
        result = await self.session.execute(stmt)
        subs = result.scalars().all()
        return [
            Subscription(
                id=sub.id,
                group_id=sub.group_id,
                notification_type=sub.notification_type,
            )
            for sub in subs
        ]
