"""
监控指标工具
2级模块：单词数=1（Metrics）
"""
import time
from typing import Dict, Any, Optional
from src.utils.logger import get_logger


class MetricsCollector:
    """指标收集器"""

    def __init__(self):
        self._metrics: Dict[str, Any] = {
            "query_count": 0,
            "query_errors": 0,
            "document_count": 0,
            "avg_query_time": 0.0,
            "total_query_time": 0.0
        }
        self._logger = get_logger()
        self._logger.debug("Metrics", "指标收集器初始化")

    def record_query(self, duration: float, success: bool = True):
        """记录查询指标"""
        self._metrics["query_count"] += 1
        if not success:
            self._metrics["query_errors"] += 1
        
        self._metrics["total_query_time"] += duration
        self._metrics["avg_query_time"] = (
            self._metrics["total_query_time"] / self._metrics["query_count"]
        )

    def record_documents(self, count: int):
        """记录文档数量"""
        self._metrics["document_count"] += count

    def get_metrics(self) -> Dict[str, Any]:
        """获取所有指标"""
        return self._metrics.copy()

    def reset(self):
        """重置指标"""
        for key in self._metrics:
            self._metrics[key] = 0
