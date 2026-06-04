"""
Config模块常量实现
2级模块：ConstantImpl，核心单词数=1（Constant）
后缀Impl不计入单词统计
禁止public，仅模块内可见
"""
from Config.interfaces.IConstant import IConstant


class ConstantImpl(IConstant):
    """常量定义实现类"""

    def get_model_name(self) -> str:
        return "sentence-transformers/all-MiniLM-L6-v2"

    def get_model_path(self) -> str:
        return "./models/sentence-transformers"

    def get_chunk_size(self) -> int:
        return 500

    def get_chunk_overlap(self) -> int:
        return 50

    def get_retrieval_top_k(self) -> int:
        return 4

    def get_similarity_threshold(self) -> float:
        return 0.7
