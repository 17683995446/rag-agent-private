"""
Config模块配置实现
2级模块：ConfigImpl，核心单词数=1（Config）
后缀Impl不计入单词统计
禁止public，仅模块内可见
"""
import json
import os
from typing import Any, Optional, Dict
from Config.interfaces.IConfig import IConfig


class ConfigImpl(IConfig):
    """配置管理实现类"""

    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._offline_mode: bool = False
        self._default_config()

    def _default_config(self) -> None:
        """设置默认配置"""
        self._config["embedding_model"] = "sentence-transformers/all-MiniLM-L6-v2"
        self._config["model_path"] = "./models/sentence-transformers"
        self._config["chunk_size"] = 500
        self._config["chunk_overlap"] = 50
        self._config["top_k"] = 4
        self._config["similarity_threshold"] = 0.7
        self._config["offline_mode"] = False

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value

    def load(self, config_path: str) -> None:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                self._config.update(loaded)

    def get_all(self) -> Dict[str, Any]:
        return self._config.copy()

    def is_offline_mode(self) -> bool:
        return self._config.get("offline_mode", False)

    def get_embedding_model_name(self) -> str:
        return self._config.get("embedding_model", "all-MiniLM-L6-v2")
