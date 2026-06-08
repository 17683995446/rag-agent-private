"""
模型注册表
2级模块：单词数=2（ModelRegistry）
"""
from typing import Dict, Any, List, Optional
from src.utils.logger import get_logger


class ModelRegistry:
    """模型注册中心"""

    def __init__(self):
        self._models: Dict[str, Dict[str, Any]] = {}
        self._active_model: Optional[str] = None
        self._logger = get_logger()
        self._logger.debug("ModelRegistry", "模型注册表初始化")

    def register(self, name: str, model_type: str, config: Dict[str, Any]) -> bool:
        """注册模型"""
        self._models[name] = {
            "type": model_type,
            "config": config,
            "active": False
        }
        self._logger.info("ModelRegistry", "模型注册成功", name=name, type=model_type)
        return True

    def activate(self, name: str) -> bool:
        """激活模型"""
        if name not in self._models:
            self._logger.warning("ModelRegistry", "模型不存在", name=name)
            return False
        
        self._active_model = name
        self._logger.info("ModelRegistry", "模型已激活", name=name)
        return True

    def get_active(self) -> Optional[str]:
        """获取当前激活的模型"""
        return self._active_model

    def list_models(self) -> List[str]:
        """列出所有模型"""
        return list(self._models.keys())
