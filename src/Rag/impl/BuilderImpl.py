"""
Rag模块Builder实现
2级模块：BuilderImpl，核心单词数=1（Builder）
后缀Impl不计入单词统计
"""
from typing import Any, Optional
from Config.interfaces.IConfig import IConfig
from Config.interfaces.IConstant import IConstant
from Config.impl.ConfigImpl import ConfigImpl
from Config.impl.ConstantImpl import ConstantImpl
from Text.interfaces.ISplitter import ISplitter
from Text.interfaces.IDocument import IDocument
from Text.impl.SplitterImpl import SplitterImpl
from Text.impl.DocumentImpl import DocumentImpl
from Vector.interfaces.IEmbedding import IEmbedding
from Vector.interfaces.IStore import IStore
from Vector.impl.EmbeddingImpl import EmbeddingImpl
from Vector.impl.StoreImpl import StoreImpl
from Vector.impl.ChromaStoreImpl import ChromaStoreImpl
from Retrieve.interfaces.IRetriever import IRetriever
from Retrieve.interfaces.IBm25 import IBm25
from Retrieve.interfaces.IReranker import IReranker
from Retrieve.impl.RetrieverImpl import RetrieverImpl
from Retrieve.impl.Bm25Impl import Bm25Impl
from Retrieve.impl.RerankerImpl import RerankerImpl
from Prompt.interfaces.IEngineer import IEngineer
from Prompt.interfaces.ITemplate import ITemplate
from Prompt.interfaces.ILLM import ILLM
from Prompt.impl.EngineerImpl import EngineerImpl
from Prompt.impl.TemplateImpl import TemplateImpl
from Prompt.impl.LlmImpl import LlmImpl
from Rag.interfaces.IBuilder import IBuilder
from Rag.interfaces.IAgent import IAgent
from Rag.impl.AgentImpl import AgentImpl


class BuilderImpl(IBuilder):
    """RAG Builder实现类"""

    def __init__(self):
        self._init_references()
        self._init_collections()

    def _init_references(self) -> None:
        self._config = None
        self._constant = None
        self._splitter = None
        self._document = None

    def _init_collections(self) -> None:
        self._embedding = None
        self._store = None
        self._retriever = None
        self._bm25 = None
        self._reranker = None
        self._engineer = None
        self._template = None
        self._llm = None
        self._agent = None

    def build_agent(self) -> IAgent:
        from src.utils.logger import get_logger
        self._logger = get_logger()
        self._logger.info("Builder", "开始构建Agent")
        
        if self._agent is None:
            self._ensure_components_initialized()
            self._agent = AgentImpl(
                self._config, self._splitter, self._document,
                self._embedding, self._store, self._retriever, 
                self._engineer, self._bm25, self._llm
            )
            self._logger.info("Builder", "Agent构建完成")
        return self._agent

    def _ensure_components_initialized(self) -> None:
        """确保组件只初始化一次"""
        if self._config is None:
            self.initialize_components()

    def build_agent_advanced(self, 
                            model_name: Optional[str] = None, 
                            cache_dir: Optional[str] = None,
                            collection_name: str = "rag_documents",
                            use_reranker: bool = True) -> IAgent:
        """
        构建高级Agent（带ChromaDB、重排序等高级功能）
        """
        from src.utils.logger import get_logger
        self._logger = get_logger()
        self._logger.info("Builder", "开始构建高级Agent")
        
        if self._agent is None:
            self.initialize_components()
            
            # 使用ChromaDB替换内存存储
            try:
                self._store = ChromaStoreImpl(collection_name=collection_name)
                self._logger.info("Builder", "ChromaDB存储初始化成功")
            except Exception as e:
                self._logger.warning("Builder", f"ChromaDB初始化失败，回退到内存存储: {str(e)}")
                self._store = StoreImpl()
            
            # 尝试加载真实嵌入模型
            if model_name:
                self._embedding = EmbeddingImpl(model_name)
            
            load_success = self._embedding.load_model(cache_dir)
            if load_success:
                self._logger.info("Builder", "真实嵌入模型加载成功")
            else:
                self._logger.warning("Builder", "真实嵌入模型加载失败，使用模拟模式")
            
            # 初始化重排序器
            if use_reranker:
                self._reranker = RerankerImpl()
                self._logger.info("Builder", "重排序器已启用")
            
            # 重新初始化检索器（带重排序）
            self._retriever = RetrieverImpl(self._embedding, self._store, self._bm25, self._reranker)
            
            self._agent = AgentImpl(
                self._config, self._splitter, self._document,
                self._embedding, self._store, self._retriever, 
                self._engineer, self._bm25, self._llm
            )
            self._logger.info("Builder", "高级Agent构建完成")
        return self._agent

    def validate_config(self) -> bool:
        if self._config is None:
            return False
        return True

    def initialize_components(self) -> None:
        self._init_config()
        self._init_text_components()
        self._init_vector_components()
        self._init_retrieve_components()
        self._init_prompt_components()

    def _init_config(self) -> None:
        self._config = ConfigImpl()
        self._constant = ConstantImpl()

    def _init_text_components(self) -> None:
        self._splitter = SplitterImpl(
            self._constant.get_chunk_size(),
            self._constant.get_chunk_overlap()
        )
        self._document = DocumentImpl()

    def _init_vector_components(self) -> None:
        self._embedding = EmbeddingImpl(self._constant.get_model_name())
        self._store = StoreImpl()

    def _init_retrieve_components(self) -> None:
        self._bm25 = Bm25Impl()
        self._retriever = RetrieverImpl(self._embedding, self._store, self._bm25)

    def _init_prompt_components(self) -> None:
        self._engineer = EngineerImpl()
        self._template = TemplateImpl()
        self._llm = LlmImpl()

    def reset(self) -> None:
        self._agent = None
