"""
Vector模块嵌入配置
2级模块：单词数=1（Config）
严格遵循二叉树模块化工程规范
"""
import os
from typing import Optional
from src.utils.logger import get_logger


class EmbeddingConfig:
    """嵌入模型配置类"""

    # 默认配置
    DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
    DEFAULT_DIMENSION = 384
    DEFAULT_CACHE_DIR = None
    DEFAULT_DEVICE = "auto"  # auto, cpu, cuda, mps

    # 模型维度映射表
    MODEL_DIMENSIONS = {
        "all-MiniLM-L6-v2": 384,
        "all-mpnet-base-v2": 768,
        "all-MiniLM-L12-v2": 384,
    }

    def __init__(
        self,
        model_name: Optional[str] = None,
        dimension: Optional[int] = None,
        cache_dir: Optional[str] = None,
        device: Optional[str] = None,
    ):
        self._model_name = model_name or self.DEFAULT_MODEL_NAME
        self._cache_dir = cache_dir or self._get_default_cache_dir()
        self._device = device or self.DEFAULT_DEVICE
        self._dimension = dimension or self._get_model_dimension(self._model_name)

        self._logger = get_logger()
        self._logger.debug(
            "EmbeddingConfig",
            "配置初始化",
            model_name=self._model_name,
            dimension=self._dimension,
            device=self._device,
            cache_dir=self._cache_dir,
        )

    def _get_default_cache_dir(self) -> str:
        """获取默认缓存目录"""
        home = os.path.expanduser("~")
        default_cache = os.path.join(home, ".cache", "rag_agent", "models")
        return default_cache

    def _get_model_dimension(self, model_name: str) -> int:
        """根据模型名称获取维度"""
        return self.MODEL_DIMENSIONS.get(model_name, self.DEFAULT_DIMENSION)

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def cache_dir(self) -> str:
        return self._cache_dir

    @property
    def device(self) -> str:
        return self._device

    def validate(self) -> bool:
        """验证配置有效性"""
        try:
            if not self._model_name or len(self._model_name.strip()) == 0:
                return False

            if self._dimension <= 0:
                return False

            return True
        except Exception:
            return False
