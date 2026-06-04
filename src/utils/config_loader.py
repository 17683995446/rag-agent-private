"""
配置加载工具
2级模块：单词数=2（ConfigLoader）
"""
import os
import yaml
from typing import Dict, Any, Optional
from src.utils.logger import get_logger


class ConfigLoader:
    """YAML配置文件加载器"""

    def __init__(self, config_path: Optional[str] = None):
        self._config_path = config_path or self._find_config_file()
        self._config: Dict[str, Any] = {}
        self._logger = get_logger()
        self._logger.debug("ConfigLoader", "初始化", path=self._config_path)

    def _find_config_file(self) -> str:
        """查找配置文件"""
        possible_paths = [
            "config.yaml",
            "config.yml",
            os.path.join(os.path.dirname(__file__), "..", "..", "config.yaml"),
            os.path.join(os.path.expanduser("~"), ".rag_agent", "config.yaml"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return "config.yaml"

    def load(self) -> Dict[str, Any]:
        """加载配置文件"""
        self._logger.enter_method("ConfigLoader", "load", path=self._config_path)
        try:
            if not os.path.exists(self._config_path):
                self._logger.warning("ConfigLoader", "配置文件不存在，使用默认配置", path=self._config_path)
                self._config = self._get_default_config()
                self._logger.exit_method("ConfigLoader", "load")
                return self._config

            with open(self._config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)

            self._logger.info("ConfigLoader", "配置加载成功", path=self._config_path)
            self._logger.exit_method("ConfigLoader", "load")
            return self._config

        except Exception as e:
            self._logger.error("ConfigLoader", "配置加载失败", error=str(e))
            self._config = self._get_default_config()
            self._logger.exit_method("ConfigLoader", "load")
            return self._config

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "app": {"name": "RAG-Agent", "version": "2.0.0", "debug": False},
            "embedding": {"model_name": "all-MiniLM-L6-v2", "dimension": 384, "device": "auto"},
            "vector_store": {"type": "memory", "collection_name": "rag_documents"},
            "retrieval": {"semantic_weight": 0.6, "keyword_weight": 0.4, "top_k": 4, "use_reranker": False},
            "text_splitter": {"chunk_size": 500, "chunk_overlap": 50},
            "logging": {"level": "INFO", "format": "structured"}
        }

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项（支持点号路径）"""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
