"""
Config模块配置接口定义
1级模块：单词数=1（Config）
"""
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict


class IConfig(ABC):
    """配置管理接口"""

    @abstractmethod
    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """获取配置值"""
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        pass

    @abstractmethod
    def load(self, config_path: str) -> None:
        """加载配置文件"""
        pass

    @abstractmethod
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        pass

    @abstractmethod
    def is_offline_mode(self) -> bool:
        """检查是否离线模式"""
        pass

    @abstractmethod
    def get_embedding_model_name(self) -> str:
        """获取嵌入模型名称"""
        pass
