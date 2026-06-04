"""
Retrieve模块检索器接口定义
1级模块：单词数=1（Retriever）
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IRetriever(ABC):
    """检索器接口"""

    @abstractmethod
    def retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """检索相关文档"""
        pass

    @abstractmethod
    def hybrid_retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """混合检索"""
        pass

    @abstractmethod
    def set_semantic_weight(self, weight: float) -> None:
        """设置语义权重"""
        pass

    @abstractmethod
    def set_keyword_weight(self, weight: float) -> None:
        """设置关键词权重"""
        pass
