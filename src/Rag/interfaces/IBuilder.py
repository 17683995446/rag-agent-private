"""
Rag模块Builder接口定义
1级模块：单词数=1（Builder）
"""
from abc import ABC, abstractmethod
from typing import Any


class IBuilder(ABC):
    """RAG Builder接口"""

    @abstractmethod
    def build_agent(self) -> Any:
        """构建Agent"""
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """验证配置"""
        pass

    @abstractmethod
    def initialize_components(self) -> None:
        """初始化组件"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """重置"""
        pass
