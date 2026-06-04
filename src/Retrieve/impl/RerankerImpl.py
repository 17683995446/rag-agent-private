"""
Retrieve模块重排序实现
2级模块：单词数=1（Reranker）
后缀Impl不计入单词统计
"""
from typing import List, Dict, Any
from Retrieve.interfaces.IReranker import IReranker
from src.utils.logger import get_logger


class RerankerImpl(IReranker):
    """简单重排序实现 - 基于关键词匹配度"""

    def __init__(self):
        self._logger = get_logger()
        self._logger.debug("Reranker", "初始化")

    def rerank(self, query: str, results: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
        self._logger.enter_method("Reranker", "rerank", query=query, result_count=len(results), top_k=top_k)
        try:
            if not results:
                self._logger.warning("Reranker", "结果为空，无需重排序")
                return []

            query_words = set(query.lower().split())
            scored_results = []

            for result in results:
                text = result.get("text", "").lower()
                score = 0

                # 计算关键词匹配度
                for word in query_words:
                    if word in text:
                        score += 1

                # 归一化分数
                if len(query_words) > 0:
                    score = score / len(query_words)

                scored_results.append((score, result))

            # 按分数降序排序
            scored_results.sort(key=lambda x: x[0], reverse=True)

            # 取前top_k个
            reranked = [result for _, result in scored_results[:top_k]]

            self._logger.info("Reranker", "重排序完成", 
                            original_count=len(results), 
                            reranked_count=len(reranked))
            self._logger.exit_method("Reranker", "rerank")
            return reranked

        except Exception as e:
            self._logger.error("Reranker", "重排序失败", error=str(e))
            self._logger.exit_method("Reranker", "rerank")
            return results[:top_k]

    def is_available(self) -> bool:
        return True
