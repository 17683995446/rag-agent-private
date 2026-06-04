"""
Vector模块模型可用性检查
2级模块：单词数=1（Checker）
严格遵循二叉树模块化工程规范
"""
import importlib
from typing import Optional, Tuple
from src.utils.logger import get_logger


class EmbeddingChecker:
    """嵌入模型可用性检查工具"""

    def __init__(self):
        self._logger = get_logger()
        self._logger.debug("EmbeddingChecker", "检查器初始化")

    def check_sentence_transformers(self) -> Tuple[bool, Optional[str]]:
        """
        检查 sentence-transformers 库是否可用
        返回: (是否可用, 错误信息)
        """
        self._logger.enter_method("EmbeddingChecker", "check_sentence_transformers")
        try:
            importlib.import_module("sentence_transformers")
            self._logger.info("EmbeddingChecker", "sentence-transformers 已安装")
            self._logger.exit_method("EmbeddingChecker", "check_sentence_transformers")
            return True, None
        except ImportError as e:
            msg = "sentence-transformers 未安装，请运行: pip install sentence-transformers"
            self._logger.warning("EmbeddingChecker", msg)
            self._logger.exit_method("EmbeddingChecker", "check_sentence_transformers")
            return False, msg
        except Exception as e:
            msg = f"检查 sentence-transformers 时出错: {str(e)}"
            self._logger.error("EmbeddingChecker", msg)
            self._logger.exit_method("EmbeddingChecker", "check_sentence_transformers")
            return False, msg

    def check_torch(self) -> Tuple[bool, Optional[str]]:
        """
        检查 PyTorch 是否可用
        返回: (是否可用, 错误信息)
        """
        self._logger.enter_method("EmbeddingChecker", "check_torch")
        try:
            importlib.import_module("torch")
            self._logger.info("EmbeddingChecker", "PyTorch 已安装")
            self._logger.exit_method("EmbeddingChecker", "check_torch")
            return True, None
        except ImportError:
            msg = "PyTorch 未安装，请运行: pip install torch"
            self._logger.warning("EmbeddingChecker", msg)
            self._logger.exit_method("EmbeddingChecker", "check_torch")
            return False, msg

    def check_all_dependencies(self) -> Tuple[bool, str]:
        """
        检查所有依赖是否满足
        返回: (是否全部可用, 汇总信息)
        """
        self._logger.enter_method("EmbeddingChecker", "check_all_dependencies")

        results = []
        all_ok = True

        ok, msg = self.check_torch()
        results.append(f"PyTorch: {'✅' if ok else '❌'} {msg or ''}")
        if not ok:
            all_ok = False

        ok, msg = self.check_sentence_transformers()
        results.append(f"sentence-transformers: {'✅' if ok else '❌'} {msg or ''}")
        if not ok:
            all_ok = False

        summary = "\n".join(results)
        self._logger.info("EmbeddingChecker", "依赖检查完成", all_ok=all_ok)
        self._logger.exit_method("EmbeddingChecker", "check_all_dependencies")

        return all_ok, summary
