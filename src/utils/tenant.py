"""
多租户工具
2级模块：单词数=1（Tenant）
"""
from typing import Dict, Any, Optional
from src.utils.logger import get_logger


class TenantManager:
    """租户管理器"""

    def __init__(self):
        self._tenants: Dict[str, Dict[str, Any]] = {}
        self._logger = get_logger()
        self._logger.debug("Tenant", "租户管理器初始化")

    def create_tenant(self, tenant_id: str, config: Optional[Dict] = None) -> bool:
        """创建租户"""
        if tenant_id in self._tenants:
            self._logger.warning("Tenant", "租户已存在", tenant_id=tenant_id)
            return False
        
        self._tenants[tenant_id] = {
            "config": config or {},
            "document_count": 0,
            "query_count": 0
        }
        self._logger.info("Tenant", "租户创建成功", tenant_id=tenant_id)
        return True

    def get_tenant(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """获取租户信息"""
        return self._tenants.get(tenant_id)

    def record_query(self, tenant_id: str):
        """记录租户查询"""
        if tenant_id in self._tenants:
            self._tenants[tenant_id]["query_count"] += 1

    def list_tenants(self) -> list:
        """列出所有租户"""
        return list(self._tenants.keys())
