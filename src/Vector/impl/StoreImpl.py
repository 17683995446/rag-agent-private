"""
Vector模块存储实现
2级模块：StoreImpl，核心单词数=1（Store）
后缀Impl不计入单词统计
"""
from typing import List, Dict, Any
from Vector.interfaces.IStore import IStore
from src.utils.logger import get_logger


class StoreImpl(IStore):
    """向量存储实现类"""

    def __init__(self):
        self._vectors: List[List[float]] = []
        self._texts: List[str] = []
        self._metadatas: List[Dict[str, Any]] = []
        self._logger = get_logger()
        self._logger.debug("Store", "向量存储初始化")

    def add_vectors(self, texts: List[str], vectors: List[List[float]], metadatas: List[Dict[str, Any]]) -> None:
        self._logger.enter_method("Store", "add_vectors", text_count=len(texts), vector_count=len(vectors))
        try:
            if not texts:
                self._logger.warning("Store", "没有文本可添加")
                return
            
            if len(texts) != len(vectors) or len(texts) != len(metadatas):
                self._logger.warning("Store", "参数长度不一致", 
                                   texts=len(texts), vectors=len(vectors), metadatas=len(metadatas))
            
            self._texts.extend(texts)
            self._vectors.extend(vectors)
            self._metadatas.extend(metadatas)
            
            self._logger.info("Store", "向量添加成功", total_count=len(self._vectors))
            self._logger.exit_method("Store", "add_vectors")
        except Exception as e:
            self._logger.error("Store", "添加向量失败", exc_info=True, error=str(e))

    def similarity_search(self, query_vector: List[float], top_k: int) -> List[Dict[str, Any]]:
        self._logger.enter_method("Store", "similarity_search", top_k=top_k)
        try:
            if len(self._vectors) == 0:
                self._logger.warning("Store", "向量存储为空，无结果")
                return []
            
            results = []
            for i in range(len(self._vectors)):
                if len(results) >= top_k:
                    break
                results.append(self._create_search_result(i))
            
            self._logger.exit_method("Store", "similarity_search", len(results))
            return results
        except Exception as e:
            self._logger.error("Store", "相似度搜索失败", exc_info=True, error=str(e))
            return []

    def _create_search_result(self, index: int) -> Dict[str, Any]:
        return {
            "text": self._texts[index],
            "metadata": self._metadatas[index],
            "vector": self._vectors[index],
            "index": index
        }

    def delete_all(self) -> None:
        self._logger.enter_method("Store", "delete_all")
        try:
            count = len(self._vectors)
            self._vectors.clear()
            self._texts.clear()
            self._metadatas.clear()
            self._logger.info("Store", "已删除所有数据", deleted_count=count)
            self._logger.exit_method("Store", "delete_all")
        except Exception as e:
            self._logger.error("Store", "删除失败", exc_info=True, error=str(e))

    def get_count(self) -> int:
        count = len(self._vectors)
        self._logger.debug("Store", "获取向量数量", count=count)
        return count
