
"""
Unit tests for EmployeeService and multi-tenant safety.
Ensures correct search, add, and tenant isolation behavior.
"""
import pytest
from app.models.employee import Employee, EmployeeStatus
from app.core.db import employee_db
from app.services.employee_service import employee_service

ORG_ID = "org_test"

def setup_module(module) -> None:
    """
    Clean up test data before each test run.
    """
    with employee_db.conn.cursor() as cur:
        cur.execute("DELETE FROM employees WHERE org_id = %s OR org_id = %s", (ORG_ID, "org_other"))
        employee_db.conn.commit()

def test_add_and_search_employee() -> None:
    """
    Should add an employee and find them by search.
    """
    emp = Employee(
        id=1,
        org_id=ORG_ID,
        firstname="John",
        lastname="Doe",
        contact="1234567890",
        department="HR",
        position="Manager",
        location="NY",
        status=EmployeeStatus.ACTIVE
    )
    employee_service.add_employee(emp)
    filters = {"firstname": "John", "lastname": "Doe", "contact": None, "department": None, "position": None, "location": None, "status": None}
    results = employee_service.search_employees(ORG_ID, filters)
    assert len(results) == 1
    assert results[0]["firstname"] == "John"
    assert results[0]["lastname"] == "Doe"

def test_multi_tenant_safety() -> None:
    """
    Should not leak data between organizations.
    """
    emp2 = Employee(
        id=2,
        org_id="org_other",
        firstname="Jane",
        lastname="Smith",
        contact="9876543210",
        department="IT",
        position="Developer",
        location="SF",
        status=EmployeeStatus.ACTIVE
    )
    employee_service.add_employee(emp2)
    filters = {"firstname": "Jane", "lastname": "Smith", "contact": None, "department": None, "position": None, "location": None, "status": None}
    results = employee_service.search_employees(ORG_ID, filters)
    assert len(results) == 0
