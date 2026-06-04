"""
Vector模块模型加载器
2级模块：单词数=2（ModelLoader）
严格遵循二叉树模块化工程规范
"""
import os
from typing import Optional, Any
from src.utils.logger import get_logger


class EmbeddingModelLoader:
    """嵌入模型加载器"""

    def __init__(self, cache_dir: str):
        self._cache_dir = cache_dir
        self._logger = get_logger()
        self._logger.debug("EmbeddingModelLoader", "加载器初始化", cache_dir=cache_dir)

    def is_model_cached(self, model_name: str) -> bool:
        """
        检查模型是否已缓存在本地
        """
        self._logger.enter_method("EmbeddingModelLoader", "is_model_cached", model_name=model_name)
        try:
            model_path = os.path.join(self._cache_dir, model_name.replace("/", "_"))
            exists = os.path.exists(model_path) and len(os.listdir(model_path)) > 0
            self._logger.debug("EmbeddingModelLoader", "缓存检查完成", 
                             model_name=model_name, cached=exists, path=model_path)
            self._logger.exit_method("EmbeddingModelLoader", "is_model_cached")
            return exists
        except Exception as e:
            self._logger.error("EmbeddingModelLoader", "缓存检查失败", error=str(e))
            self._logger.exit_method("EmbeddingModelLoader", "is_model_cached")
            return False

    def load_model(self, model_name: str) -> Optional[Any]:
        """
        加载 sentence-transformers 模型
        返回模型实例或None
        """
        self._logger.enter_method("EmbeddingModelLoader", "load_model", model_name=model_name)
        try:
            from sentence_transformers import SentenceTransformer

            model_path = os.path.join(self._cache_dir, model_name.replace("/", "_"))

            if self.is_model_cached(model_name):
                self._logger.info("EmbeddingModelLoader", "从本地缓存加载模型", path=model_path)
                model = SentenceTransformer(model_path)
            else:
                self._logger.info("EmbeddingModelLoader", "从HuggingFace下载模型", model_name=model_name)
                model = SentenceTransformer(model_name, cache_folder=self._cache_dir)

            self._logger.info("EmbeddingModelLoader", "模型加载成功", model_name=model_name)
            self._logger.exit_method("EmbeddingModelLoader", "load_model")
            return model

        except Exception as e:
            self._logger.error("EmbeddingModelLoader", "模型加载失败", 
                             model_name=model_name, error=str(e))
            self._logger.exit_method("EmbeddingModelLoader", "load_model")
            return None
