from collections import defaultdict
from typing import Any

import httpx
from nonebot import logger
from typing_extensions import Self

from nonebot_plugin_ba_tools.features.student.domain.model.birthday import Birthday
from nonebot_plugin_ba_tools.features.student.domain.model.student import Student
from nonebot_plugin_ba_tools.features.student.domain.port.student_data_gateway import (
    StudentDataGateway,
)

SCHALEDB_API_URL = "https://schaledb.com"
HTTP_TIMEOUT = 30.0


class SchaleDBService(StudentDataGateway):
    """SchaleDB API 客户端网关实现

    处理 SchaleDB 返回的学生数据，包括多形态学生的合并。
    """

    def __init__(
        self,
        base_url: str = SCHALEDB_API_URL,
        timeout: float = HTTP_TIMEOUT,
    ) -> None:
        """初始化服务

        Args:
            base_url: SchaleDB API 的基础 URL
            timeout: HTTP 请求超时时间
        """
        self.base_url = base_url
        self.timeout = httpx.Timeout(timeout)
        self.client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Self:
        """异步上下文管理器入口"""
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """异步上下文管理器出口"""
        if self.client:
            await self.client.aclose()
            self.client = None

    async def fetch_all_students(self) -> list[Student]:
        """从 SchaleDB 获取所有学生信息

        返回的学生列表已合并同一个人的多个形态。具有相同 PersonalName 和
        FamilyName 的多个学生条目会被合并为一个 Student 对象，其 avatars
        列表包含该人所有形态的头像 URL。

        Returns:
            list[Student]: 学生信息列表

        Raises:
            httpx.RequestError: 网络请求失败
            ValueError: 数据格式不符合预期
        """
        if not self.client:
            msg = "Service not initialized. Use 'async with' context manager."
            raise RuntimeError(msg)

        try:
            # TODO: 可做i18n
            response = await self.client.get("/data/zh/students.json")
            response.raise_for_status()

            data = response.json()
            students: list[Student] = []

            if not isinstance(data, dict):
                msg = f"意外的数据格式，期望字典，收到 {type(data).__name__}"
                raise ValueError(msg)

            # 临时存储已解析的学生数据，用于合并同一个人的多个形态
            # 键: (personal_name, family_name)，值: 该人的所有形态数据
            students_by_name: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(
                list
            )

            for student_id_str, student_data in data.items():
                try:
                    personal_name = student_data.get("PersonalName")
                    family_name = student_data.get("FamilyName")

                    if personal_name is None or family_name is None:
                        logger.warning(
                            f"跳过学生 (ID: {student_id_str}): "
                            f"缺少 PersonalName 或 FamilyName"
                        )
                        continue

                    # 按 (PersonalName, FamilyName) 分组
                    key = (str(personal_name), str(family_name))
                    students_by_name[key].append(student_data)

                except (KeyError, TypeError) as e:
                    logger.warning(f"跳过处理学生数据 (ID: {student_id_str}): {e}")
                    continue

            # 为每个人合并多个形态
            for (personal_name, family_name), forms_data in students_by_name.items():
                try:
                    student = self._merge_student_forms(
                        personal_name, family_name, forms_data
                    )
                    students.append(student)
                except (KeyError, ValueError, TypeError) as e:
                    logger.warning(
                        f"跳过合并学生形态 ({personal_name} {family_name}): {e}"
                    )
                    continue

            logger.info(f"成功获取 {len(students)} 个学生信息")

        except httpx.RequestError as e:
            logger.error(f"网络请求失败: {e}")
            raise

        return students

    @staticmethod
    def _merge_student_forms(
        personal_name: str, family_name: str, forms_data: list[dict[str, Any]]
    ) -> Student:
        """合并同一个人的多个形态

        Args:
            personal_name: 学生的个人名称
            family_name: 学生的家族名称
            forms_data: 该学生的所有形态数据列表

        Returns:
            Student: 合并后的学生模型，包含该人所有形态的头像

        Raises:
            ValueError: 数据格式不符合预期
        """
        if not forms_data:
            raise ValueError("学生形态数据列表为空")

        # 使用第一个形态的数据作为基础信息来源
        primary_form = forms_data[0]

        # 提取学生 ID
        student_id_value = primary_form.get("Id")
        if student_id_value is None:
            raise ValueError("缺少学生 Id 字段")
        student_id = int(student_id_value)

        # 获取学生名称
        name = str(family_name) + str(personal_name)

        # 提取别名（SchaleDB 似乎没有专门的别名字段）
        nicknames: list[str] = []

        # 提取生日（只保留月和日）
        birthday_str = primary_form.get("BirthDay") or primary_form.get("Birthday")
        birthday = None
        if birthday_str:
            try:
                birthday = Birthday.from_date_string(birthday_str)
            except ValueError as e:
                logger.warning(
                    f"无法解析学生 {student_id} 的生日: {birthday_str} - {e}"
                )
                birthday = None

        # 收集所有形态的头像
        avatars: list[str] = []
        for form_data in forms_data:
            try:
                id = form_data.get("Id")
                if id:
                    avatar_url = (
                        f"{SCHALEDB_API_URL}/images/student/collection/{id}.webp"
                    )
                    avatars.append(avatar_url)
            except (KeyError, TypeError) as e:
                logger.warning(f"无法解析学生 {student_id} 的头像: {e}")
                continue

        if not avatars:
            logger.warning(
                f"学生 {student_id} ({personal_name} {family_name}) 没有有效的头像"
            )

        # 提取扩展字段
        school = primary_form.get("School")
        club = primary_form.get("Club")
        star_grade = primary_form.get("StarGrade")
        squad_type = primary_form.get("SquadType")
        tactic_role = primary_form.get("TacticRole")
        position = primary_form.get("Position")
        bullet_type = primary_form.get("BulletType")
        armor_type = primary_form.get("ArmorType")
        weapon_type = primary_form.get("WeaponType")
        character_age = primary_form.get("CharacterAge")
        height = primary_form.get("CharHeightMetric")
        birthday_display = primary_form.get("Birthday")
        character_voice = primary_form.get("CharacterVoice")
        illustrator = primary_form.get("Illustrator")
        hobby = primary_form.get("Hobby")
        profile_introduction = primary_form.get("ProfileIntroduction")
        street_adaptation = primary_form.get("StreetBattleAdaptation")
        outdoor_adaptation = primary_form.get("OutdoorBattleAdaptation")
        indoor_adaptation = primary_form.get("IndoorBattleAdaptation")

        return Student(
            id=student_id,
            name=name,
            nicknames=nicknames,
            birthday=birthday,
            avatars=avatars,
            school=str(school) if school else None,
            club=str(club) if club else None,
            star_grade=int(star_grade) if star_grade is not None else None,
            squad_type=str(squad_type) if squad_type else None,
            tactic_role=str(tactic_role) if tactic_role else None,
            position=str(position) if position else None,
            bullet_type=str(bullet_type) if bullet_type else None,
            armor_type=str(armor_type) if armor_type else None,
            weapon_type=str(weapon_type) if weapon_type else None,
            character_age=str(character_age) if character_age else None,
            height=str(height) if height else None,
            birthday_str=str(birthday_display) if birthday_display else None,
            character_voice=str(character_voice) if character_voice else None,
            illustrator=str(illustrator) if illustrator else None,
            hobby=str(hobby) if hobby else None,
            profile_introduction=str(profile_introduction) if profile_introduction else None,
            street_adaptation=int(street_adaptation) if street_adaptation is not None else None,
            outdoor_adaptation=int(outdoor_adaptation) if outdoor_adaptation is not None else None,
            indoor_adaptation=int(indoor_adaptation) if indoor_adaptation is not None else None,
        )

    @staticmethod
    def _parse_student(data: dict[str, Any]) -> Student:
        """解析单个学生数据为 Student 模型（已弃用）

        此方法保留用于兼容性，建议使用 _merge_student_forms 代替。

        Args:
            data: 学生数据字典

        Returns:
            Student: 解析后的学生模型

        Raises:
            ValueError: 数据格式不符合预期
        """
        # 提取学生 ID
        student_id_value = data.get("Id")
        if student_id_value is None:
            raise ValueError("缺少学生 Id 字段")
        student_id = int(student_id_value)

        # 提取学生名称
        # name_value = data.get("PersonalName") or data.get("DevName") or data.get("Name")
        # if name_value is None:
        #     raise ValueError("缺少学生名称字段")
        family_name = data.get("FamilyName")
        personal_name = data.get("PersonalName")
        name = (
            f"{family_name} {personal_name}" if family_name and personal_name else None
        )
        if name is None:
            raise ValueError("缺少学生名称字段")

        # 提取别名（SchaleDB 似乎没有专门的别名字段）
        nicknames: list[str] = []

        # 提取生日（只保留月和日）
        birthday_str = data.get("BirthDay") or data.get("Birthday")
        birthday = None
        if birthday_str:
            try:
                birthday = Birthday.from_date_string(birthday_str)
            except ValueError as e:
                logger.warning(f"无法解析学生 {name} 的生日: {birthday_str} - {e}")
                birthday = None

        # 提取头像（从 Icon 字段）
        avatars: list[str] = []
        avatar_url = f"{SCHALEDB_API_URL}/images/student/collection/{student_id}.webp"
        avatars.append(avatar_url)

        return Student(
            id=student_id,
            name=name,
            nicknames=nicknames,
            birthday=birthday,
            avatars=avatars,
        )


async def fetch_students_from_schaledb() -> list[Student]:
    """从 SchaleDB 获取所有学生数据

    返回的学生列表已合并同一个人的多个形态。

    Returns:
        list[Student]: 学生列表

    Raises:
        httpx.RequestError: 网络请求失败
        ValueError: 数据解析失败
    """
    async with SchaleDBService() as service:
        return await service.fetch_all_students()
