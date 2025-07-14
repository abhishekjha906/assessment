
"""
Tenant service for multi-tenant safety and organization validation.
Extendable for real DB-backed org validation.
"""
from app.models.organization import Organization
from typing import Optional

class TenantService:
    @staticmethod
    def validate_org(org_id: str) -> bool:
        """
        Validate organization ID for multi-tenant safety.
        Extend to check org existence in DB for production.
        :param org_id: Organization ID
        :return: True if valid, False otherwise
        """
        return isinstance(org_id, str) and len(org_id.strip()) > 0

tenant_service = TenantService()
