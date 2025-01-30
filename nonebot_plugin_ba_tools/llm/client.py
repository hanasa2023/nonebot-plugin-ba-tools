from __future__ import annotations

import json
from pathlib import Path

import aiofiles
import yaml
from nonebot import logger
from openai import APIStatusError, AsyncOpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
)

from ..config import LLM_DIR
from .models import Presets, Prompt
from .utils import str_presenter


class Chat:
    def __init__(self, api_key: str, base_url: str, preset_path: Path, model: str) -> None:
        """创建Chat实例

        Args:
            api_key (str): 模型的api key
            base_url (str): 模型的endpoint
            promot_path (Path): 预设存储路径
            model (str): 接入的模型
        """
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model
        self.presets: list[str] = []
        self.preset_path = preset_path
        self.prompt_content = ""
        self.__load_preset()

    def __load_preset(self) -> None:
        """加载预设"""
        # 若llm文件夹不存在，则创建
        self.preset_path.parent.mkdir(parents=True, exist_ok=True)

        # 若未找到预设文件，则从模板创建
        if not self.preset_path.exists():
            prompts: Path = Path(__file__).parent / "prompts.yaml"
            data: str = ""
            with open(prompts) as f:
                data += f.read()
            with open(self.preset_path, "w") as f:
                f.write(data)
            logger.info("未找到内置预设，已自动生成")

        self.__get_prompt_content(preset=None)

    def __get_prompt_content(self, preset: str | None) -> None:
        """从给定的预设文件中读取系统提示词"""
        presets: Presets
        with open(self.preset_path) as f:
            data = yaml.safe_load(f)
            logger.debug(data)
            presets = Presets(
                current_preset=data["current_preset"],
                presets=data["presets"],
                prompts=[Prompt(**promot) for promot in data["prompts"]],
            )

        self.presets = presets.presets
        self.prompt_content = next(
            prompt.content
            for prompt in presets.prompts
            if prompt.name == (preset if preset else presets.current_preset)
        )

    async def chat(self, session_id: str, current_message: str) -> str | None:
        """创建会话

        Args:
            session_id (str): 会话id
            current_message (str): 当前用户消息

        Returns:
            str | None: llm返回的内容
        """
        try:
            session_data: Path = LLM_DIR / f"sessions/{session_id}.json"
            # 如果没有则创建对话记录文件夹
            session_data.parent.mkdir(parents=True, exist_ok=True)

            messages: list[ChatCompletionMessageParam] = []
            # 获取对话记录
            if session_data.exists():
                async with aiofiles.open(session_data, "r+") as f:
                    msgs = json.loads(await f.read())
                    for msg in msgs:
                        messages.append(msg)
            messages.append({"role": "user", "content": current_message})

            messages.insert(0, {"role": "system", "content": self.prompt_content})
            logger.debug(f"messages: {messages}")

            response: ChatCompletion = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=1.3,
            )
            ccm: ChatCompletionMessage = response.choices[0].message

            # 保存对话记录
            messages.pop(0)
            messages.append({"role": ccm.role, "content": ccm.content})
            async with aiofiles.open(session_data, "w") as f:
                await f.write(json.dumps(messages))

            return ccm.content
        except APIStatusError as e:
            # 处理 API 错误
            logger.info(f"APIStatusError: {e}")
            if e.status_code == 400:
                return "请求体格式错误"
            elif e.status_code == 401:
                return "API 密钥无效"
            elif e.status_code == 402:
                return "抱歉，API 账户余额不足，请联系管理员充值。"
            elif e.status_code == 422:
                return "请求体参数错误"
            elif e.status_code == 429:
                return "请求频率过高"
            elif e.status_code == 500:
                return "服务器错误"
            elif e.status_code == 503:
                return "服务器繁忙"
            else:
                return f"API调用错误: {e}"
        except Exception as e:
            return f"发生错误: {e}"

    def reset_preset(self) -> str:
        """重置预设

        Returns:
            str: 重置状态
        """
        if self.preset_path.exists():
            self.preset_path.unlink()
        self.__load_preset()
        return "重置预设成功"

    # TODO: 支持更换会话场景预设
    def change_preset(self, new_preset: str) -> str:
        """更换预设

        Args:
            new_preset (str): 新的预设名

        Returns:
            str: 预设更新状态
        """
        if new_preset not in self.presets:
            return "预设不存在，保持原预设"
        else:
            self.__get_prompt_content(new_preset)
            return f"预设已更改为: {new_preset}"

    async def create_new_prompt(self, preset_name: str, prompt_content) -> str:
        """创建新预设

        Args:
            preset_name (str): 预设名
            prompt_content (_type_): 提示词内容

        Returns:
            str: 创建状态
        """
        try:
            yaml.add_representer(str, str_presenter, Dumper=yaml.SafeDumper)
            async with aiofiles.open(self.preset_path) as f:
                data = yaml.safe_load(await f.read())
            async with aiofiles.open(self.preset_path, "w") as f:
                data["presets"].append(preset_name)
                data["prompts"].append({"name": preset_name, "content": prompt_content})
                yaml_str = yaml.safe_dump(
                    data,
                    allow_unicode=True,
                    indent=2,
                    sort_keys=False,
                    encoding="utf-8",
                ).decode("utf-8")
                await f.write(yaml_str)
                self.presets.append(preset_name)
            return f"预设 {preset_name} 已创建"
        except Exception as e:
            return f"发生错误：{e}"

    def clear_session(self, session_id: str) -> str:
        """清除历史会话消息

        Args:
            session_id (str): 会话id

        Returns:
            str: 清除状态
        """
        session_data: Path = LLM_DIR / f"sessions/{session_id}.json"
        if session_data.exists():
            session_data.unlink()
            return "对话记录已清除"
        else:
            return "没有对话记录"
