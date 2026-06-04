"""
Retrieve模块BM25实现
2级模块：Bm25Impl，核心单词数=1（Bm25）
后缀Impl不计入单词统计
"""
from typing import List, Dict, Any
from Retrieve.interfaces.IBm25 import IBm25
from src.utils.logger import get_logger


class Bm25Impl(IBm25):
    """BM25检索实现类"""

    def __init__(self):
        self._documents: List[str] = []
        self._index: Dict[str, List[int]] = {}
        self._logger = get_logger()
        self._logger.debug("BM25", "BM25索引初始化")

    def index_documents(self, documents: List[str]) -> None:
        self._logger.enter_method("BM25", "index_documents", doc_count=len(documents))
        try:
            if not documents:
                self._logger.warning("BM25", "无文档可索引")
                return
            
            self._documents = documents
            self._build_index()
            self._logger.info("BM25", "索引构建完成", doc_count=len(documents), index_size=len(self._index))
            self._logger.exit_method("BM25", "index_documents")
        except Exception as e:
            self._logger.error("BM25", "索引构建失败", exc_info=True, error=str(e))

    def search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        self._logger.enter_method("BM25", "search", query=query, top_k=top_k)
        try:
            if not query:
                self._logger.warning("BM25", "查询为空")
                return []
            
            if len(self._documents) == 0:
                self._logger.warning("BM25", "索引为空，无结果")
                return []
            
            # 使用索引搜索，而不是遍历所有文档
            query_words = query.lower().split()
            candidate_indices = set()
            
            for word in query_words:
                if word in self._index:
                    candidate_indices.update(self._index[word])
            
            # 对候选文档进行匹配
            results = []
            for i in candidate_indices:
                doc = self._documents[i]
                if self._match_query(query, doc):
                    results.append(self._create_result(doc, i))
                    if len(results) >= top_k:
                        break
            
            # 如果候选不够，回退到完整遍历（兜底）
            if len(results) < top_k:
                for i, doc in enumerate(self._documents):
                    if i not in candidate_indices and self._match_query(query, doc):
                        results.append(self._create_result(doc, i))
                        if len(results) >= top_k:
                            break
            
            self._logger.exit_method("BM25", "search", len(results))
            return results
        except Exception as e:
            self._logger.error("BM25", "搜索失败", exc_info=True, error=str(e))
            return []

    def _match_query(self, query: str, doc: str) -> bool:
        return query.lower() in doc.lower()

    def _create_result(self, doc: str, index: int) -> Dict[str, Any]:
        return {"text": doc, "score": 1.0, "index": index}

    def add_to_index(self, documents: List[str]) -> None:
        self._logger.enter_method("BM25", "add_to_index", doc_count=len(documents))
        try:
            if not documents:
                self._logger.warning("BM25", "无文档可添加")
                return
            
            start_idx = len(self._documents)
            self._documents.extend(documents)
            
            # 增量构建索引
            for i, doc in enumerate(documents):
                doc_idx = start_idx + i
                words = doc.lower().split()
                for word in words:
                    if word not in self._index:
                        self._index[word] = []
                    self._index[word].append(doc_idx)
            
            self._logger.info("BM25", "增量索引完成", added_count=len(documents), 
                             total_count=len(self._documents))
            self._logger.exit_method("BM25", "add_to_index")
        except Exception as e:
            self._logger.error("BM25", "增量索引失败", exc_info=True, error=str(e))

    def clear_index(self) -> None:
        self._logger.enter_method("BM25", "clear_index")
        try:
            count = len(self._documents)
            self._documents.clear()
            self._index.clear()
            self._logger.info("BM25", "索引已清除", cleared_count=count)
            self._logger.exit_method("BM25", "clear_index")
        except Exception as e:
            self._logger.error("BM25", "清除索引失败", exc_info=True, error=str(e))

    def get_index_size(self) -> int:
        size = len(self._documents)
        self._logger.debug("BM25", "获取索引大小", size=size)
        return size

    def _build_index(self) -> None:
        self._index.clear()
        for i, doc in enumerate(self._documents):
            words = doc.lower().split()
            for word in words:
                if word not in self._index:
                    self._index[word] = []
                self._index[word].append(i)
