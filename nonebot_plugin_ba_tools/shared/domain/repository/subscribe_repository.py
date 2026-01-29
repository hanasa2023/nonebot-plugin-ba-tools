from abc import ABC, abstractmethod

from nonebot_plugin_ba_tools.shared.domain.model.subscription import (
    Subscription,
    SubscriptionNotificationType,
)


class SubscribeRepository(ABC):
    """用户订阅仓库"""

    @abstractmethod
    async def add_subscribe(
        self, group_id: str, notification_type: SubscriptionNotificationType
    ) -> None:
        """添加订阅

        Args:
            group_id (str): 群号
            feature_name (SubscriptionFeatureType): 功能类型
        """

        raise NotImplementedError

    @abstractmethod
    async def remove_subscribe(
        self, group_id: str, notification_type: SubscriptionNotificationType
    ) -> None:
        """移除订阅

        Args:
            group_id (str): 群号
            feature_name (SubscriptionFeatureType): 功能类型
        """

        raise NotImplementedError

    @abstractmethod
    async def get_subscribed_groups(
        self, notification_type: SubscriptionNotificationType
    ) -> list[Subscription]:
        """获取已订阅某功能的群组列表

        Args:
            feature_name (SubscriptionFeatureType): 功能类型

        Returns:
            list[Subscription]: 已订阅某功能的群组列表
        """

        raise NotImplementedError
