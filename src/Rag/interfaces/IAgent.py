"""
Rag模块Agent接口定义
1级模块：单词数=1（Agent）
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IAgent(ABC):
    """RAG Agent接口"""

    @abstractmethod
    def query(self, question: str) -> str:
        """查询"""
        pass

    @abstractmethod
    def add_documents(self, documents: List[str]) -> None:
        """添加文档"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """重置"""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        """检查是否就绪"""
        pass
