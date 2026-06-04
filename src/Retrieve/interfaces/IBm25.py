"""
Retrieve模块BM25接口定义
1级模块：单词数=1（Bm25）
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IBm25(ABC):
    """BM25检索接口"""

    @abstractmethod
    def index_documents(self, documents: List[str]) -> None:
        """索引文档（替换）"""
        pass

    @abstractmethod
    def add_to_index(self, documents: List[str]) -> None:
        """增量添加到索引"""
        pass

    @abstractmethod
    def search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        pass

    @abstractmethod
    def clear_index(self) -> None:
        """清除索引"""
        pass

    @abstractmethod
    def get_index_size(self) -> int:
        """获取索引大小"""
        pass
