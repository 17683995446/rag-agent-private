"""
Prompt模块LLM接口定义
1级模块：单词数=1（LLM）
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class ILLM(ABC):
    """大语言模型接口"""

    @abstractmethod
    def generate(self, prompt: str, context: List[str]) -> str:
        """基于上下文生成回答"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查模型是否可用"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """获取模型名称"""
        pass
