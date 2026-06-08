"""
Vector模块嵌入实现
2级模块：EmbeddingImpl，核心单词数=1（Embedding）
后缀Impl不计入单词统计
"""
from typing import List, Optional, Any
from Vector.interfaces.IEmbedding import IEmbedding
from src.utils.logger import get_logger


class EmbeddingImpl(IEmbedding):
    """嵌入模型实现类 - 支持真实sentence-transformers"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self._model_name = model_name
        self._dimension = 384
        self._model: Optional[Any] = None
        self._is_available = False
        self._logger = get_logger()
        self._logger.debug("Embedding", "嵌入模型初始化", model_name=self._model_name, available=self._is_available)
        # 预加载numpy避免运行时重复导入
        self._numpy = None
        self._load_numpy()

    def _load_numpy(self) -> bool:
        """预加载numpy库"""
        try:
            import numpy as np
            self._numpy = np
            return True
        except ImportError:
            self._logger.warning("Embedding", "numpy未安装")
            return False

    def load_model(self, cache_dir: Optional[str] = None) -> bool:
        """
        加载真实嵌入模型
        返回是否加载成功
        """
        self._logger.enter_method("Embedding", "load_model", model_name=self._model_name)
        try:
            # 检查依赖
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError:
                self._logger.warning("Embedding", "sentence-transformers未安装，使用模拟模式")
                self._logger.exit_method("Embedding", "load_model")
                return False

            # 加载模型
            if cache_dir:
                self._model = SentenceTransformer(self._model_name, cache_folder=cache_dir)
            else:
                self._model = SentenceTransformer(self._model_name)

            # 获取实际维度
            self._dimension = self._model.get_sentence_embedding_dimension()
            self._is_available = True

            self._logger.info("Embedding", "模型加载成功",
                            model_name=self._model_name,
                            dimension=self._dimension)
            self._logger.exit_method("Embedding", "load_model")
            return True

        except Exception as e:
            self._logger.error("Embedding", "模型加载失败", error=str(e))
            self._is_available = False
            self._logger.exit_method("Embedding", "load_model")
            return False

    def embed_text(self, text: str) -> List[float]:
        self._logger.enter_method("Embedding", "embed_text", text_len=len(text) if text else 0)
        try:
            if not text:
                self._logger.warning("Embedding", "空文本，返回零向量")
                return [0.0] * self._dimension

            if self._is_available and self._model is not None:
                # 使用真实模型
                embedding = self._model.encode(text, convert_to_numpy=True)
                result = embedding.tolist()
                self._logger.exit_method("Embedding", "embed_text")
                return result
            else:
                # 降级到模拟模式
                self._logger.warning("Embedding", "模型不可用，返回模拟零向量")
                return [0.0] * self._dimension

        except Exception as e:
            self._logger.error("Embedding", "文本嵌入失败", exc_info=True, error=str(e))
            return [0.0] * self._dimension

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        self._logger.enter_method("Embedding", "embed_texts", text_count=len(texts))
        try:
            if not texts:
                self._logger.warning("Embedding", "空列表，返回空结果")
                return []

            if self._is_available and self._model is not None:
                # 使用真实模型批量嵌入
                embeddings = self._model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
                results = [emb.tolist() for emb in embeddings]
                self._logger.exit_method("Embedding", "embed_texts", len(results))
                return results
            else:
                # 降级到模拟模式
                results = [self.embed_text(text) for text in texts]
                self._logger.exit_method("Embedding", "embed_texts", len(results))
                return results

        except Exception as e:
            self._logger.error("Embedding", "批量嵌入失败", exc_info=True, error=str(e))
            return []

    def get_dimension(self) -> int:
        self._logger.debug("Embedding", "获取向量维度", dimension=self._dimension)
        return self._dimension

    def is_available(self) -> bool:
        return self._is_available
