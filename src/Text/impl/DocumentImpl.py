"""
Text模块文档实现
2级模块：DocumentImpl，核心单词数=1（Document）
后缀Impl不计入单词统计
"""
from typing import List, Dict, Any
from Text.interfaces.IDocument import IDocument


class DocumentImpl(IDocument):
    """文档实现类"""

    def create_document(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "content": content,
            "metadata": metadata,
            "content_length": len(content)
        }

    def get_content(self, document: Dict[str, Any]) -> str:
        return document.get("content", "")

    def get_metadata(self, document: Dict[str, Any]) -> Dict[str, Any]:
        return document.get("metadata", {})

    def batch_create(self, contents: List[str], metadatas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        documents = []
        for i, content in enumerate(contents):
            metadata = metadatas[i] if i < len(metadatas) else {}
            doc = self.create_document(content, metadata)
            documents.append(doc)
        return documents
