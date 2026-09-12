import math
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, RoleChecker
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.dashboard import PaginatedAuditLogResponse, AuditLogResponse

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

@router.get("", response_model=PaginatedAuditLogResponse, dependencies=[Depends(RoleChecker(["ADMIN"]))])
def get_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    action: Optional[str] = None,
    module: Optional[str] = None,
    username: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)

    if action:
        query = query.filter(AuditLog.action == action)
    if module:
        query = query.filter(AuditLog.module == module)
    if username:
        query = query.filter(AuditLog.username.like(f"%{username.strip()}%"))

    total = query.count()
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    logs = query.order_by(AuditLog.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedAuditLogResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=logs
    )
