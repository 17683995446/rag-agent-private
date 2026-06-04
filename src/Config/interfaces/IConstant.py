"""
Config模块常量接口定义
1级模块：单词数=1（Constant）
接口文件前缀I不计入单词统计
"""
from abc import ABC, abstractmethod


class IConstant(ABC):
    """常量定义接口"""

    @abstractmethod
    def get_model_name(self) -> str:
        """获取模型名称"""
        pass

    @abstractmethod
    def get_model_path(self) -> str:
        """获取模型路径"""
        pass

    @abstractmethod
    def get_chunk_size(self) -> int:
        """获取分块大小"""
        pass

    @abstractmethod
    def get_chunk_overlap(self) -> int:
        """获取分块重叠"""
        pass

    @abstractmethod
    def get_retrieval_top_k(self) -> int:
        """获取检索top_k"""
        pass

    @abstractmethod
    def get_similarity_threshold(self) -> float:
        """获取相似度阈值"""
        pass
