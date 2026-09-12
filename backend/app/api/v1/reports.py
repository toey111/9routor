from typing import Optional
from fastapi import APIRouter, Depends, Query, Response, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.api.deps import get_db, get_current_user, RoleChecker
from app.models.user import User
from app.models.personnel import Personnel
from app.services.export_service import (
    export_personnel_csv,
    export_personnel_excel,
    export_personnel_pdf
)
from app.services.audit_service import log_audit

router = APIRouter(prefix="/reports", tags=["Reports & Export"])

@router.get("/export", dependencies=[Depends(RoleChecker(["ADMIN", "EXECUTIVE"]))])
def export_personnel_data(
    format: str = Query("excel", regex="^(excel|csv|pdf)$"),
    department_id: Optional[int] = None,
    branch_id: Optional[int] = None,
    position_id: Optional[int] = None,
    personnel_type_id: Optional[int] = None,
    work_status: Optional[str] = None,
    search: Optional[str] = None,
    request: Request = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Personnel)

    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Personnel.first_name_th.like(search_pattern),
                Personnel.last_name_th.like(search_pattern),
                Personnel.personnel_code.like(search_pattern),
                Personnel.email.like(search_pattern)
            )
        )
    if department_id:
        query = query.filter(Personnel.department_id == department_id)
    if branch_id:
        query = query.filter(Personnel.branch_id == branch_id)
    if position_id:
        query = query.filter(Personnel.position_id == position_id)
    if personnel_type_id:
        query = query.filter(Personnel.personnel_type_id == personnel_type_id)
    if work_status:
        query = query.filter(Personnel.work_status == work_status)

    personnel_list = query.order_by(Personnel.id.asc()).all()

    log_audit(
        db=db,
        username=current_user.username,
        action="EXPORT",
        module="REPORT",
        description=f"Export รายงานบุคลากร รูปแบบ {format.upper()} จำนวน {len(personnel_list)} รายการ",
        user_id=current_user.id,
        request=request
    )

    if format == "csv":
        csv_stream = export_personnel_csv(personnel_list)
        return Response(
            content=csv_stream.getvalue().encode('utf-8-sig'),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=personnel_report.csv"}
        )
    elif format == "pdf":
        pdf_stream = export_personnel_pdf(personnel_list)
        return StreamingResponse(
            pdf_stream,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=personnel_report.pdf"}
        )
    else: # excel
        excel_stream = export_personnel_excel(personnel_list)
        return StreamingResponse(
            excel_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=personnel_report.xlsx"}
        )
