
"""
Employee service for business logic related to employee search and management.
Handles DB interaction and logging.
"""

"""
Employee service for business logic related to employee search and management.
Uses EmployeeSearchService for DB logic, supports pagination and sorting.
"""

from app.core.config import logger
from app.models.employee import Employee
from app.services.employee_search import EmployeeSearchService
from app.core.db import get_db_conn
from typing import List, Dict, Any, Optional, Tuple


class EmployeeService:
    @staticmethod

    def search_employees(
        org_id: str,
        filters: Dict[str, Any],
        columns: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "id",
        sort_order: str = "asc",
        db_conn=None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Search employees for an organization with filters, pagination, and sorting.
        :return: Tuple of results and total count
        """
        service = EmployeeSearchService(db_conn)
        results, total = service.search(org_id, filters, columns, page, page_size, sort_by, sort_order)
        return results, total

    @staticmethod
    def add_employee(employee: Employee, db_conn=None) -> None:
        """
        Add an employee to the database.
        """
        service = EmployeeSearchService(db_conn)
        service.add_employee(employee)
        logger.info(f"Employee {employee.id} added for org {employee.org_id}")

employee_service = EmployeeService()
