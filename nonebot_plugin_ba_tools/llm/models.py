from dataclasses import dataclass


@dataclass
class Prompt:
    name: str
    content: str


@dataclass
class Presets:
    current_preset: str
    presets: list[str]
    prompts: list[Prompt]
