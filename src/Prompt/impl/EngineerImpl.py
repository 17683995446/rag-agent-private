"""
Prompt模块Prompt工程师实现
2级模块：EngineerImpl，核心单词数=1（Engineer）
后缀Impl不计入单词统计
"""
from typing import List, Dict, Any
from Prompt.interfaces.IEngineer import IEngineer


class EngineerImpl(IEngineer):
    """Prompt工程师实现类"""

    def __init__(self):
        self._instructions: List[str] = []
        self._default_instruction = "你是一个智能助手，请根据提供的上下文回答问题。"

    def build_prompt(self, query: str, context: List[str]) -> str:
        context_str = self.format_context(context)
        system_prompt = self.build_system_prompt()
        return f"{system_prompt}\n\n上下文：\n{context_str}\n\n问题：{query}"

    def build_system_prompt(self) -> str:
        instructions = "\n".join(self._instructions) if self._instructions else self._default_instruction
        return f"{instructions}"

    def format_context(self, context: List[str]) -> str:
        if not context:
            return "没有找到相关上下文。"
        formatted = []
        for i, ctx in enumerate(context, 1):
            formatted.append(f"[{i}] {ctx}")
        return "\n".join(formatted)

    def add_instructions(self, instructions: List[str]) -> None:
        self._instructions.extend(instructions)
