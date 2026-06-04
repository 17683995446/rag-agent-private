"""
Text模块分片实现
2级模块：SplitterImpl，核心单词数=1（Splitter）
后缀Impl不计入单词统计
"""
from typing import List
from Text.interfaces.ISplitter import ISplitter
from src.utils.logger import get_logger


class SplitterImpl(ISplitter):
    """文本分片实现类"""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self._chunk_size = max(1, chunk_size)
        self._chunk_overlap = max(0, min(chunk_overlap, self._chunk_size - 1))
        self._logger = get_logger()
        self._logger.debug("Splitter", "初始化分片器", chunk_size=self._chunk_size, overlap=self._chunk_overlap)

    def split_text(self, text: str) -> List[str]:
        self._logger.enter_method("Splitter", "split_text", text_len=len(text) if text else 0)
        try:
            if not text:
                self._logger.warning("Splitter", "空文本，跳过分片")
                return []
            
            chunks = []
            start = 0
            text_len = len(text)
            
            while start < text_len:
                chunks.extend(self._process_chunk(text, start))
                start = start + self._chunk_size - self._chunk_overlap
            
            result = [c for c in chunks if c]
            self._logger.exit_method("Splitter", "split_text", len(result))
            return result
        except Exception as e:
            self._logger.error("Splitter", "文本分片失败", exc_info=True, error=str(e))
            return []

    def _process_chunk(self, text: str, start: int) -> List[str]:
        end = start + self._chunk_size
        chunk = text[start:end]
        return [chunk.strip()] if chunk.strip() else []

    def split_documents(self, documents: List[str]) -> List[str]:
        self._logger.enter_method("Splitter", "split_documents", doc_count=len(documents))
        try:
            all_chunks = []
            for i, doc in enumerate(documents):
                chunks = self.split_text(doc)
                all_chunks.extend(chunks)
            self._logger.exit_method("Splitter", "split_documents", len(all_chunks))
            return all_chunks
        except Exception as e:
            self._logger.error("Splitter", "文档分片失败", exc_info=True, error=str(e))
            return []

    def set_chunk_size(self, size: int) -> None:
        self._logger.debug("Splitter", "设置分块大小", old_size=self._chunk_size, new_size=size)
        self._chunk_size = max(1, size)
        if self._chunk_overlap >= self._chunk_size:
            self._chunk_overlap = self._chunk_size - 1

    def set_chunk_overlap(self, overlap: int) -> None:
        self._logger.debug("Splitter", "设置重叠大小", old_overlap=self._chunk_overlap, new_overlap=overlap)
        self._chunk_overlap = max(0, min(overlap, self._chunk_size - 1))
