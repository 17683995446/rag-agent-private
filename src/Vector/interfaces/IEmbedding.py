"""
Vector模块嵌入接口定义
1级模块：单词数=1（Embedding）
"""
from abc import ABC, abstractmethod
from typing import List


class IEmbedding(ABC):
    """嵌入模型接口"""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """嵌入单个文本"""
        pass

    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """嵌入多个文本"""
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """获取向量维度"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查模型是否可用"""
        pass
