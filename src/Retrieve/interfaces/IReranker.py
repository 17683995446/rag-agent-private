"""
Retrieve模块重排序接口定义
1级模块：单词数=1（Reranker）
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IReranker(ABC):
    """重排序器接口"""

    @abstractmethod
    def rerank(self, query: str, results: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
        """对检索结果进行重排序"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查是否可用"""
        pass
