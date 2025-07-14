
"""
Organization model for multi-tenancy in HR Employee Search API.
Represents an organization/tenant.
"""
from typing import Any

class Organization:
    def __init__(self, org_id: str, name: str) -> None:
        """
        Initialize an organization.
        :param org_id: Organization ID
        :param name: Organization name
        """
        self.org_id = org_id
        self.name = name
