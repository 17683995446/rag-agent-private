"""
Rag模块Agent实现
2级模块：AgentImpl，核心单词数=1（Agent）
后缀Impl不计入单词统计
"""
from typing import List, Dict, Any, Optional
from Config.interfaces.IConfig import IConfig
from Text.interfaces.ISplitter import ISplitter
from Text.interfaces.IDocument import IDocument
from Vector.interfaces.IEmbedding import IEmbedding
from Vector.interfaces.IStore import IStore
from Retrieve.interfaces.IRetriever import IRetriever
from Retrieve.interfaces.IBm25 import IBm25
from Prompt.interfaces.IEngineer import IEngineer
from Prompt.interfaces.ILLM import ILLM
from Rag.interfaces.IAgent import IAgent
from src.utils.logger import get_logger


class AgentImpl(IAgent):
    """RAG Agent实现类"""

    def __init__(self, config: IConfig, splitter: ISplitter, document: IDocument,
                 embedding: IEmbedding, store: IStore, retriever: IRetriever, 
                 engineer: IEngineer, bm25: IBm25, llm: Optional[ILLM] = None):
        self._config = config
        self._splitter = splitter
        self._document = document
        self._embedding = embedding
        self._store = store
        self._retriever = retriever
        self._engineer = engineer
        self._bm25 = bm25
        self._llm = llm
        self._document_count = 0
        self._logger = get_logger()
        self._logger.info("Agent", "Agent初始化完成", llm_available=llm is not None)

    def query(self, question: str) -> str:
        self._logger.enter_method("Agent", "query", question=question)
        try:
            if not question or question.strip() == "":
                self._logger.warning("Agent", "查询为空")
                return "[错误] 查询不能为空"
            
            retrieved = self._retriever.retrieve(question, top_k=4)
            self._logger.debug("Agent", "检索到相关文档", count=len(retrieved))
            
            contexts = [doc.get("text", "") for doc in retrieved if doc.get("text")]
            
            # 如果有LLM，使用LLM生成回答
            if self._llm and self._llm.is_available():
                prompt = self._engineer.build_prompt(question, contexts)
                result = self._llm.generate(prompt, contexts)
                self._logger.info("Agent", "使用LLM生成回答")
            else:
                # 模拟模式
                prompt = self._engineer.build_prompt(question, contexts)
                result = f"[模拟回答]\n{prompt}"
            
            self._logger.exit_method("Agent", "query", result)
            return result
        except Exception as e:
            self._logger.error("Agent", "查询失败", exc_info=True, error=str(e))
            return f"[错误] 查询失败: {str(e)}"

    def add_documents(self, documents: List[str]) -> None:
        self._logger.enter_method("Agent", "add_documents", doc_count=len(documents))
        try:
            if not documents:
                self._logger.warning("Agent", "文档列表为空")
                self._logger.exit_method("Agent", "add_documents")
                return
            
            valid_docs = [doc for doc in documents if doc and doc.strip()]
            if len(valid_docs) < len(documents):
                self._logger.warning("Agent", "跳过空文档", skipped=len(documents)-len(valid_docs))
            
            if not valid_docs:
                self._logger.warning("Agent", "无有效文档可添加")
                self._logger.exit_method("Agent", "add_documents")
                return
            
            chunks = self._splitter.split_documents(valid_docs)
            self._logger.debug("Agent", "文本分片完成", chunk_count=len(chunks))
            
            if not chunks:
                self._logger.warning("Agent", "分片结果为空")
                self._logger.exit_method("Agent", "add_documents")
                return
            
            # 记录原始状态（用于异常回滚）
            original_doc_count = self._document_count
            original_vector_count = self._store.get_count()
            original_bm25_size = self._bm25.get_index_size()
            
            try:
                metadatas = [{"index": i, "source_doc_index": i} for i in range(len(chunks))]
                vectors = self._embedding.embed_texts(chunks)
                
                self._store.add_vectors(chunks, vectors, metadatas)
                self._logger.debug("Agent", "向量存储完成")
                
                # 增量索引 BM25
                self._bm25.add_to_index(chunks)
                self._logger.debug("Agent", "BM25增量索引完成")
                
                self._document_count += len(valid_docs)
                self._logger.info("Agent", "文档添加成功", added_count=len(valid_docs), 
                                 total_docs=self._document_count, chunks=len(chunks))
                
                self._logger.exit_method("Agent", "add_documents")
                
            except Exception as inner_e:
                # 事务回滚：尝试恢复到原始状态
                self._logger.error("Agent", "添加文档添加过程异常，尝试回滚", error=str(inner_e))
                try:
                    # 尝试回滚
                    current_vector_count = self._store.get_count()
                    if current_vector_count > original_vector_count:
                        self._logger.warning("Agent", "向量存储已部分写入，无法精确回滚")
                    
                    self._document_count = original_doc_count
                    self._logger.warning("Agent", "文档计数已回滚")
                except Exception as rollback_e:
                    self._logger.error("Agent", "回滚失败", error=str(rollback_e))
                
                raise inner_e
                
        except Exception as e:
            self._logger.error("Agent", "添加文档失败", exc_info=True, error=str(e))

    def reset(self) -> None:
        self._logger.enter_method("Agent", "reset")
        try:
            # 顺序重置，确保尽可能清理
            reset_ok = True
            
            try:
                self._store.delete_all()
                self._logger.debug("Agent", "向量存储已清理")
            except Exception as e:
                self._logger.error("Agent", "向量存储清理失败", error=str(e))
                reset_ok = False
            
            try:
                self._bm25.clear_index()
                self._logger.debug("Agent", "BM25索引已清理")
            except Exception as e:
                self._logger.error("Agent", "BM25索引清理失败", error=str(e))
                reset_ok = False
            
            # 无论如何都重置计数
            self._document_count = 0
            
            if reset_ok:
                self._logger.info("Agent", "重置完成")
            else:
                self._logger.warning("Agent", "重置完成但有部分失败")
            
            self._logger.exit_method("Agent", "reset")
        except Exception as e:
            self._logger.error("Agent", "重置失败", exc_info=True, error=str(e))

    def get_status(self) -> Dict[str, Any]:
        status = {
            "document_count": self._document_count,
            "vector_count": self._store.get_count(),
            "bm25_index_size": self._bm25.get_index_size(),
            "embedding_available": self._embedding.is_available(),
            "offline_mode": self._config.is_offline_mode()
        }
        self._logger.debug("Agent", "获取状态", status=status)
        return status

    def is_ready(self) -> bool:
        ready = self._embedding.is_available() and self._store.get_count() > 0
        self._logger.debug("Agent", "检查就绪状态", ready=ready)
        return ready
