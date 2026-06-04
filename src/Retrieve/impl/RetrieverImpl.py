"""
Retrieve模块检索器实现
2级模块：RetrieverImpl，核心单词数=1（Retriever）
后缀Impl不计入单词统计
"""
from typing import List, Dict, Any, Optional
from Retrieve.interfaces.IRetriever import IRetriever
from Vector.interfaces.IEmbedding import IEmbedding
from Vector.interfaces.IStore import IStore
from Retrieve.interfaces.IBm25 import IBm25
from Retrieve.interfaces.IReranker import IReranker
from src.utils.logger import get_logger


class RetrieverImpl(IRetriever):
    """检索器实现类"""

    def __init__(self, embedding: IEmbedding, store: IStore, bm25: IBm25, reranker: Optional[IReranker] = None):
        self._semantic_weight = 0.6
        self._keyword_weight = 0.4
        self._embedding = embedding
        self._store = store
        self._bm25 = bm25
        self._reranker = reranker
        self._logger = get_logger()
        self._logger.debug("Retriever", "初始化检索器", semantic_weight=self._semantic_weight, keyword_weight=self._keyword_weight, has_reranker=reranker is not None)

    def retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        self._logger.enter_method("Retriever", "retrieve", query=query, top_k=top_k)
        try:
            semantic_results = self._semantic_search(query, top_k)
            keyword_results = self._keyword_search(query, top_k)
            combined = self._combine_results(semantic_results, keyword_results, top_k)
            
            # 如果配置了重排序器，进行重排序
            if self._reranker and self._reranker.is_available() and combined:
                self._logger.info("Retriever", "启用重排序")
                combined = self._reranker.rerank(query, combined, top_k)
            
            self._logger.exit_method("Retriever", "retrieve", len(combined))
            return combined
        except Exception as e:
            self._logger.error("Retriever", "检索失败", exc_info=True, error=str(e))
            return []

    def hybrid_retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        return self.retrieve(query, top_k)

    def set_semantic_weight(self, weight: float) -> None:
        self._logger.debug("Retriever", "设置语义权重", old_weight=self._semantic_weight, new_weight=weight)
        self._semantic_weight = max(0.0, min(1.0, weight))
        self._keyword_weight = 1.0 - self._semantic_weight
        self._logger.debug("Retriever", "权重已更新", semantic_weight=self._semantic_weight, keyword_weight=self._keyword_weight)

    def set_keyword_weight(self, weight: float) -> None:
        self._logger.debug("Retriever", "设置关键词权重", old_weight=self._keyword_weight, new_weight=weight)
        self._keyword_weight = max(0.0, min(1.0, weight))
        self._semantic_weight = 1.0 - self._keyword_weight
        self._logger.debug("Retriever", "权重已更新", semantic_weight=self._semantic_weight, keyword_weight=self._keyword_weight)

    def _semantic_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        self._logger.enter_method("Retriever", "_semantic_search", query=query, top_k=top_k)
        if not self._embedding.is_available():
            self._logger.warning("Retriever", "语义检索跳过：嵌入模型不可用")
            return []
        
        query_vector = self._embedding.embed_text(query)
        results = self._store.similarity_search(query_vector, top_k)
        for result in results:
            result["type"] = "semantic"
            result["weight"] = self._semantic_weight
        self._logger.exit_method("Retriever", "_semantic_search", len(results))
        return results

    def _keyword_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        self._logger.enter_method("Retriever", "_keyword_search", query=query, top_k=top_k)
        if self._bm25.get_index_size() == 0:
            self._logger.warning("Retriever", "关键词检索跳过：BM25索引为空")
            return []
        
        results = self._bm25.search(query, top_k)
        for result in results:
            result["type"] = "keyword"
            result["weight"] = self._keyword_weight
        self._logger.exit_method("Retriever", "_keyword_search", len(results))
        return results

    def _combine_results(self, semantic_results: List[Dict[str, Any]], 
                        keyword_results: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
        self._logger.enter_method("Retriever", "_combine_results", semantic_count=len(semantic_results), 
                                  keyword_count=len(keyword_results), top_k=top_k)
        
        # 使用权重排序合并
        all_results = []
        seen_texts = set()
        
        for result in semantic_results + keyword_results:
            text = result.get("text", "")
            if text not in seen_texts:
                seen_texts.add(text)
                all_results.append(result)
        
        # 按权重和类型排序（语义优先）
        all_results.sort(key=lambda x: (-x.get("weight", 0), 0 if x.get("type") == "semantic" else 1))
        combined = all_results[:top_k]
        
        self._logger.exit_method("Retriever", "_combine_results", len(combined))
        return combined
