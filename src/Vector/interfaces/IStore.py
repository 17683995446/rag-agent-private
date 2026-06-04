"""
Vector模块存储接口定义
1级模块：单词数=1（Store）
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IStore(ABC):
    """向量存储接口"""

    @abstractmethod
    def add_vectors(self, texts: List[str], vectors: List[List[float]], metadatas: List[Dict[str, Any]]) -> None:
        """添加向量"""
        pass

    @abstractmethod
    def similarity_search(self, query_vector: List[float], top_k: int) -> List[Dict[str, Any]]:
        """相似度搜索"""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """删除所有数据"""
        pass

    @abstractmethod
    def get_count(self) -> int:
        """获取向量数量"""
        pass
