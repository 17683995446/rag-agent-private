"""
Vector模块缓存工具
2级模块：单词数=1（Cache）
严格遵循二叉树模块化工程规范
"""
import os
from typing import Optional
from src.utils.logger import get_logger


class EmbeddingCache:
    """嵌入模型缓存工具类"""

    def __init__(self, cache_dir: str):
        self._cache_dir = cache_dir
        self._logger = get_logger()
        self._logger.debug("EmbeddingCache", "缓存工具初始化", cache_dir=self._cache_dir)

    def ensure_cache_dir(self) -> bool:
        """
        确保缓存目录存在
        返回True表示目录已创建或已存在
        """
        self._logger.enter_method("EmbeddingCache", "ensure_cache_dir", cache_dir=self._cache_dir)
        try:
            if not os.path.exists(self._cache_dir):
                os.makedirs(self._cache_dir, exist_ok=True)
                self._logger.info("EmbeddingCache", "缓存目录已创建", directory=self._cache_dir)
            else:
                self._logger.debug("EmbeddingCache", "缓存目录已存在", directory=self._cache_dir)

            self._logger.exit_method("EmbeddingCache", "ensure_cache_dir")
            return True
        except Exception as e:
            self._logger.error("EmbeddingCache", "创建缓存目录失败", exc_info=True, error=str(e))
            return False

    def get_cache_dir(self) -> str:
        """获取缓存目录路径"""
        return self._cache_dir

    def is_writable(self) -> bool:
        """检查目录是否可写"""
        try:
            test_file = os.path.join(self._cache_dir, ".write_test")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except Exception:
            return False
