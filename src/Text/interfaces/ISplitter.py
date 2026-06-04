"""
Text模块分片接口定义
1级模块：单词数=1（Splitter）
"""
from abc import ABC, abstractmethod
from typing import List


class ISplitter(ABC):
    """文本分片接口"""

    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        """分割单个文本"""
        pass

    @abstractmethod
    def split_documents(self, documents: List[str]) -> List[str]:
        """分割多个文档"""
        pass

    @abstractmethod
    def set_chunk_size(self, size: int) -> None:
        """设置分块大小"""
        pass

    @abstractmethod
    def set_chunk_overlap(self, overlap: int) -> None:
        """设置分块重叠"""
        pass
