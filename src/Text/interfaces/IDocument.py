"""
Text模块文档接口定义
1级模块：单词数=1（Document）
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IDocument(ABC):
    """文档接口"""

    @abstractmethod
    def create_document(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """创建文档"""
        pass

    @abstractmethod
    def get_content(self, document: Dict[str, Any]) -> str:
        """获取文档内容"""
        pass

    @abstractmethod
    def get_metadata(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """获取文档元数据"""
        pass

    @abstractmethod
    def batch_create(self, contents: List[str], metadatas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量创建文档"""
        pass
