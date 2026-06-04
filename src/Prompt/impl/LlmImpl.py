"""
Prompt模块LLM实现
2级模块：单词数=1（Llm）
后缀Impl不计入单词统计
"""
from typing import List, Dict, Any, Optional
from Prompt.interfaces.ILLM import ILLM
from src.utils.logger import get_logger


class LlmImpl(ILLM):
    """模拟LLM实现类"""

    def __init__(self, model_name: str = "mock-llm"):
        self._model_name = model_name
        self._is_available = False
        self._logger = get_logger()
        self._logger.debug("LLM", "初始化", model_name=self._model_name)

    def generate(self, prompt: str, context: List[str]) -> str:
        self._logger.enter_method("LLM", "generate", prompt_len=len(prompt), context_count=len(context))
        try:
            if not context:
                result = "[模拟回答] 未找到相关上下文。"
            else:
                context_preview = " ".join(context)[:200]
                result = f"[模拟回答] 基于以下上下文：{context_preview}..."

            self._logger.exit_method("LLM", "generate")
            return result
        except Exception as e:
            self._logger.error("LLM", "生成失败", error=str(e))
            return "[错误] 生成回答时出错。"

    def is_available(self) -> bool:
        return self._is_available

    def get_model_name(self) -> str:
        return self._model_name
