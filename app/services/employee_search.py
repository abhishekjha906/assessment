"""
Employee search service: all DB logic for employee search, add, pagination, and sorting.
Uses DB connection as dependency, not singleton. Handles edge cases and logs actions.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings, logger
from app.models.employee import Employee, EmployeeStatus
from typing import List, Dict, Any, Optional, Tuple


class EmployeeSearchService:
    """
    Service for employee DB operations: add, search, pagination, sorting.
    Uses DB connection as dependency. Handles edge cases and logs actions.
    ORM-like structure using SQL and Python objects.
    """
    def __init__(self, db_conn):
        self.conn = db_conn

    def add_employee(self, employee: Employee) -> None:
        """
        Add an employee to the database. Handles rollback and logs errors.
        """
        if not isinstance(employee, Employee):
            logger.error("add_employee: Invalid employee object.")
            raise ValueError("Invalid employee object.")
        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO employees (org_id, firstname, lastname, contact, department, position, location, status, extra)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    employee.org_id,
                    employee.firstname,
                    employee.lastname,
                    employee.contact,
                    employee.department,
                    employee.position,
                    employee.location,
                    employee.status.value,
                    employee.extra
                ))
                self.conn.commit()
                logger.info(f"Employee {employee.firstname} {employee.lastname} added to DB (org: {employee.org_id})")
        except Exception as e:
            logger.error(f"Failed to add employee: {e}")
            self.conn.rollback()
            raise

    def search(
        self,
        org_id: str,
        filters: Dict[str, Any],
        columns: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "id",
        sort_order: str = "asc"
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Search employees with filters, pagination, and sorting.
        Returns results and total count. Handles SQL errors and logs actions.
        """
        if not org_id or not isinstance(org_id, str):
            logger.error("search: Invalid org_id.")
            return [], 0
        if page < 1:
            logger.warning(f"search: Invalid page {page}, defaulting to 1.")
            page = 1
        if page_size < 1 or page_size > 100:
            logger.warning(f"search: Invalid page_size {page_size}, defaulting to 20.")
            page_size = 20
        query = "SELECT * FROM employees WHERE org_id = %s"
        params = [org_id]
        for k, v in filters.items():
            if v is not None:
                query += f" AND {k} = %s"
                params.append(v.value if isinstance(v, EmployeeStatus) else v)
        # Sorting
        allowed_sort = {"id", "firstname", "lastname", "department", "position", "location", "status"}
        if sort_by not in allowed_sort:
            logger.warning(f"search: Invalid sort_by '{sort_by}', defaulting to 'id'.")
            sort_by = "id"
        sort_order = "desc" if sort_order.lower() == "desc" else "asc"
        query += f" ORDER BY {sort_by} {sort_order}"
        # Pagination
        offset = (page - 1) * page_size
        query += " LIMIT %s OFFSET %s"
        params.extend([page_size, offset])
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
                # Get total count
                count_query = "SELECT COUNT(*) FROM employees WHERE org_id = %s"
                count_params = [org_id]
                for k, v in filters.items():
                    if v is not None:
                        count_query += f" AND {k} = %s"
                        count_params.append(v.value if isinstance(v, EmployeeStatus) else v)
                cur.execute(count_query, count_params)
                total = cur.fetchone()["count"]
            results = []
            for row in rows:
                data = dict(row)
                if columns:
                    data = {k: v for k, v in data.items() if k in columns}
                results.append(data)
            logger.info(f"Search returned {len(results)} results for org {org_id}, page {page}, page_size {page_size}, sort_by {sort_by} {sort_order}")
            return results, total
        except Exception as e:
            logger.error(f"Failed to search employees: {e}")
            return [], 0
