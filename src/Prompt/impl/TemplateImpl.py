"""
Prompt模块模板实现
2级模块：TemplateImpl，核心单词数=1（Template）
后缀Impl不计入单词统计
"""
from typing import Dict, Any
from Prompt.interfaces.ITemplate import ITemplate


class TemplateImpl(ITemplate):
    """Prompt模板实现类"""

    def __init__(self):
        self._templates: Dict[str, str] = self._default_templates()

    def _default_templates(self) -> Dict[str, str]:
        return {
            "default": "上下文：{context}\n\n问题：{question}\n\n回答：",
            "detailed": "你是一个专家助手。请根据以下上下文详细回答问题。\n\n上下文：\n{context}\n\n问题：{question}\n\n请提供详细的回答：",
            "concise": "基于：{context}\n\n回答：{question}"
        }

    def get_template(self, template_name: str) -> str:
        return self._templates.get(template_name, self._templates["default"])

    def render(self, template_name: str, variables: Dict[str, Any]) -> str:
        template = self.get_template(template_name)
        return template.format(**variables)

    def list_templates(self) -> list:
        return list(self._templates.keys())

    def add_template(self, name: str, template: str) -> None:
        self._templates[name] = template
