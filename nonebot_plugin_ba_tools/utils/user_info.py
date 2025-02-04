from __future__ import annotations

from ..config import SUPERUSERS


def is_group_owner(user_info: dict[str, str]) -> bool:
    return user_info.get("role") == "owner"


def is_group_admin(user_info: dict[str, str]) -> bool:
    return user_info.get("role") == "admin"


def is_superuser(user_id: int | str) -> bool:
    return str(user_id) in SUPERUSERS
