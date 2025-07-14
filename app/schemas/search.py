
"""
Pydantic schemas for employee search API request and response.
Supports filtering and dynamic output columns.
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.models.employee import EmployeeStatus

class EmployeeSearchRequest(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    contact: Optional[str]
    department: Optional[str]
    position: Optional[str]
    location: Optional[str]
    status: Optional[EmployeeStatus]
    columns: Optional[List[str]]  # dynamic output columns

class EmployeeSearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total: int
