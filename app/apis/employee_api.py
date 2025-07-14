
"""
API router for employee search endpoints.
Handles rate limiting, multi-tenant safety, and search logic.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.search import EmployeeSearchRequest, EmployeeSearchResponse
from app.services.employee_service import employee_service
from app.services.tenant_service import tenant_service
from app.core.config import logger

from app.core.rate_limit import rate_limiter
from app.models.employee import EmployeeStatus
from app.core.db import get_db_conn
from fastapi import Depends

router = APIRouter()

async def check_rate_limit(request: Request) -> str:
    """
    Dependency to enforce rate limiting per organization.
    :param request: FastAPI request
    :return: org_id if allowed
    :raises HTTPException: if missing org_id or rate limit exceeded
    """
    org_id = request.headers.get("X-Org-Id")
    if not org_id:
        logger.error("Missing X-Org-Id header")
        raise HTTPException(status_code=400, detail="Missing organization header")
    if not rate_limiter.is_allowed(org_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return org_id


@router.post("/search", response_model=EmployeeSearchResponse, tags=["Employee"])
async def search_employees(
    req: EmployeeSearchRequest,
    org_id: str = Depends(check_rate_limit),
    db_conn=Depends(get_db_conn),
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "id",
    sort_order: str = "asc"
) -> EmployeeSearchResponse:
    """
    Search employees with filters, dynamic columns, pagination, and sorting.
    Multi-tenant safety enforced by org_id.
    Status filter uses EmployeeStatus enum: Active, Not Started, Terminated.
    :param req: Search request body
    :param org_id: Organization ID from header
    :param page: Page number (default 1)
    :param page_size: Results per page (default 20)
    :param sort_by: Column to sort by (default id)
    :param sort_order: asc or desc (default asc)
    :return: Search response
    """
    # Validate organization
    if not tenant_service.validate_org(org_id):
        logger.error(f"Invalid organization: {org_id}")
        raise HTTPException(status_code=403, detail="Invalid organization")

    # Prepare filters
    filters = {
        "firstname": req.firstname,
        "lastname": req.lastname,
        "contact": req.contact,
        "department": req.department,
        "position": req.position,
        "location": req.location,
        "status": req.status,
    }
    columns = req.columns

    # Search employees with pagination and sorting
    results, total = employee_service.search_employees(
        org_id, filters, columns, page, page_size, sort_by, sort_order, db_conn=db_conn
    )
    logger.info(f"Search returned {len(results)} results for org {org_id}, page {page}")
    db_conn.close()
    return EmployeeSearchResponse(results=results, total=total)
