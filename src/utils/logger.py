"""
RAG Agent 日志工具
提供统一的日志记录功能，方便调试和问题发现
"""
import logging
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

class Logger:
    """统一日志管理类"""

    _instance: Optional['Logger'] = None
    _initialized: bool = False

    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not Logger._initialized:
            self._setup_logger()
            Logger._initialized = True

    def _setup_logger(self) -> None:
        """设置日志格式和输出"""
        self.logger = logging.getLogger("RAG_Agent")
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self, module: str, message: str, **kwargs: Any) -> None:
        """记录DEBUG级别日志"""
        if kwargs:
            msg = f"[{module}] {message} | {kwargs}"
        else:
            msg = f"[{module}] {message}"
        self.logger.debug(msg)

    def info(self, module: str, message: str, **kwargs: Any) -> None:
        """记录INFO级别日志"""
        if kwargs:
            msg = f"[{module}] {message} | {kwargs}"
        else:
            msg = f"[{module}] {message}"
        self.logger.info(msg)

    def warning(self, module: str, message: str, **kwargs: Any) -> None:
        """记录WARNING级别日志"""
        if kwargs:
            msg = f"[{module}] {message} | {kwargs}"
        else:
            msg = f"[{module}] {message}"
        self.logger.warning(msg)

    def error(self, module: str, message: str, exc_info: bool = False, **kwargs: Any) -> None:
        """记录ERROR级别日志"""
        if kwargs:
            msg = f"[{module}] {message} | {kwargs}"
        else:
            msg = f"[{module}] {message}"
        self.logger.error(msg, exc_info=exc_info)

    def critical(self, module: str, message: str, **kwargs: Any) -> None:
        """记录CRITICAL级别日志"""
        if kwargs:
            msg = f"[{module}] {message} | {kwargs}"
        else:
            msg = f"[{module}] {message}"
        self.logger.critical(msg)

    def enter_method(self, module: str, method: str, **kwargs: Any) -> None:
        """记录方法进入"""
        self.debug(module, f"进入 {method}", params=kwargs)

    def exit_method(self, module: str, method: str, result: Any = None) -> None:
        """记录方法退出"""
        self.debug(module, f"退出 {method}", result_type=type(result).__name__)

    def log_state(self, module: str, state: Dict[str, Any]) -> None:
        """记录状态信息"""
        self.info(module, "当前状态", state=state)

# 单例全局日志实例
_logger = Logger()

def get_logger() -> Logger:
    """获取全局日志实例"""
    return _logger
