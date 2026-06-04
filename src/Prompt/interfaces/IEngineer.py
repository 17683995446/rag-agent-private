"""
Prompt模块Prompt工程师接口定义
1级模块：单词数=1（Engineer）
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IEngineer(ABC):
    """Prompt工程师接口"""

    @abstractmethod
    def build_prompt(self, query: str, context: List[str]) -> str:
        """构建Prompt"""
        pass

    @abstractmethod
    def build_system_prompt(self) -> str:
        """构建系统Prompt"""
        pass

    @abstractmethod
    def format_context(self, context: List[str]) -> str:
        """格式化上下文"""
        pass

    @abstractmethod
    def add_instructions(self, instructions: List[str]) -> None:
        """添加指令"""
        pass
