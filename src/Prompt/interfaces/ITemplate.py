"""
Prompt模块模板接口定义
1级模块：单词数=1（Template）
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class ITemplate(ABC):
    """Prompt模板接口"""

    @abstractmethod
    def get_template(self, template_name: str) -> str:
        """获取模板"""
        pass

    @abstractmethod
    def render(self, template_name: str, variables: Dict[str, Any]) -> str:
        """渲染模板"""
        pass

    @abstractmethod
    def list_templates(self) -> list:
        """列出所有模板"""
        pass

    @abstractmethod
    def add_template(self, name: str, template: str) -> None:
        """添加模板"""
        pass
