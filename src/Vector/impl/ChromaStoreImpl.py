"""
Vector模块ChromaDB存储实现
2级模块：单词数=2（ChromaStore）
严格遵循二叉树模块化工程规范
"""
import os
import uuid
from typing import List, Dict, Any, Optional
from Vector.interfaces.IStore import IStore
from src.utils.logger import get_logger


class ChromaStoreImpl(IStore):
    """ChromaDB向量存储实现"""

    def __init__(self, collection_name: str = "rag_documents", persist_dir: Optional[str] = None):
        self._collection_name = collection_name
        self._persist_dir = persist_dir or os.path.join(os.path.expanduser("~"), ".cache", "rag_agent", "chroma")
        self._client = None
        self._collection = None
        self._logger = get_logger()
        self._logger.debug("ChromaStore", "初始化", collection=collection_name, persist_dir=self._persist_dir)
        self._init_client()

    def _init_client(self) -> bool:
        """初始化ChromaDB客户端"""
        try:
            import chromadb
            self._client = chromadb.PersistentClient(path=self._persist_dir)
            self._collection = self._client.get_or_create_collection(name=self._collection_name)
            self._logger.info("ChromaStore", "客户端初始化成功")
            return True
        except Exception as e:
            self._logger.error("ChromaStore", "客户端初始化失败", error=str(e))
            return False

    def add_vectors(self, texts: List[str], vectors: List[List[float]], metadatas: List[Dict[str, Any]]) -> None:
        self._logger.enter_method("ChromaStore", "add_vectors", text_count=len(texts))
        try:
            if not texts or not vectors:
                self._logger.warning("ChromaStore", "空数据，跳过添加")
                return

            ids = [str(uuid.uuid4()) for _ in texts]
            self._collection.add(
                ids=ids,
                documents=texts,
                embeddings=vectors,
                metadatas=metadatas
            )
            self._logger.info("ChromaStore", "向量添加成功", total_count=self.get_count())
            self._logger.exit_method("ChromaStore", "add_vectors")
        except Exception as e:
            self._logger.error("ChromaStore", "向量添加失败", exc_info=True, error=str(e))

    def search(self, query_vector: List[float], top_k: int) -> List[Dict[str, Any]]:
        """兼容旧接口的搜索方法"""
        return self.similarity_search(query_vector, top_k)

    def similarity_search(self, query_vector: List[float], top_k: int) -> List[Dict[str, Any]]:
        self._logger.enter_method("ChromaStore", "similarity_search", top_k=top_k)
        try:
            # 防御性检查：空查询向量
            if not query_vector or len(query_vector) == 0:
                self._logger.warning("ChromaStore", "查询向量为空，返回空结果")
                self._logger.exit_method("ChromaStore", "similarity_search", 0)
                return []

            # 防御性检查：空集合
            if self.get_count() == 0:
                self._logger.warning("ChromaStore", "集合为空，返回空结果")
                self._logger.exit_method("ChromaStore", "similarity_search", 0)
                return []

            results = self._collection.query(
                query_embeddings=[query_vector],
                n_results=top_k
            )

            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        "text": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0.0,
                        "type": "semantic"
                    })

            self._logger.exit_method("ChromaStore", "similarity_search", len(formatted_results))
            return formatted_results
        except Exception as e:
            self._logger.error("ChromaStore", "搜索失败", exc_info=True, error=str(e))
            return []

    def delete_all(self) -> None:
        self._logger.enter_method("ChromaStore", "delete_all")
        try:
            all_ids = self._collection.get()["ids"]
            if all_ids:
                self._collection.delete(ids=all_ids)
            self._logger.info("ChromaStore", "所有向量已删除")
            self._logger.exit_method("ChromaStore", "delete_all")
        except Exception as e:
            self._logger.error("ChromaStore", "删除失败", exc_info=True, error=str(e))

    def get_count(self) -> int:
        try:
            return self._collection.count()
        except Exception:
            return 0
