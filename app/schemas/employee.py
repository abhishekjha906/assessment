
"""
Pydantic schema for employee API output.
Supports extra fields for dynamic columns.
"""
from pydantic import BaseModel
from typing import Optional
from app.models.employee import EmployeeStatus

class EmployeeOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    contact: str
    department: str
    position: str
    location: str
    status: EmployeeStatus
    # Extra fields allowed for dynamic columns
    class Config:
        extra = "allow"
