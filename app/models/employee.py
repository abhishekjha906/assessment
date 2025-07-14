
"""
Employee model and status enum for HR Employee Search API.
Represents an employee record and supports dynamic output columns.
"""
from typing import Optional, Dict, Any, List
from enum import Enum

class EmployeeStatus(str, Enum):
    """Allowed status values for employees."""
    ACTIVE = "Active"
    NOT_STARTED = "Not Started"
    TERMINATED = "Terminated"

class Employee:
    """
    Employee data model for PostgreSQL storage and API output.
    """
    def __init__(
        self,
        id: int,
        org_id: str,
        firstname: str,
        lastname: str,
        contact: str,
        department: str,
        position: str,
        location: str,
        status: EmployeeStatus,
        extra: Optional[Dict[str, Any]] = None
    ) -> None:
        self.id = id
        self.org_id = org_id
        self.firstname = firstname
        self.lastname = lastname
        self.contact = contact
        self.department = department
        self.position = position
        self.location = location
        self.status = status
        self.extra = extra or {}

    def to_dict(self, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Convert employee to dict, optionally filtering by columns.
        :param columns: List of columns to include
        :return: Dict representation
        """
        data = {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "contact": self.contact,
            "department": self.department,
            "position": self.position,
            "location": self.location,
            "status": self.status.value,
        }
        data.update(self.extra)
        if columns:
            return {k: v for k, v in data.items() if k in columns}
        return data
