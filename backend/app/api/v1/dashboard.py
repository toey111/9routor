from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db, get_current_user, RoleChecker
from app.models.user import User
from app.models.personnel import Personnel
from app.models.master_data import Branch, PersonnelType
from app.models.academic import AcademicPosition, EducationHistory
from app.schemas.dashboard import DashboardStatsResponse, KeyValueStat

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStatsResponse, dependencies=[Depends(RoleChecker(["ADMIN", "EXECUTIVE"]))])
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_personnel = db.query(Personnel).count()

    # Academic vs Support staff
    # Academic: type 1, 2 (ข้าราชการ/พนักงานสายวิชาการ), Support: 3, 4, 5
    academic_staff_count = db.query(Personnel).filter(Personnel.personnel_type_id.in_([1, 2])).count()
    support_staff_count = total_personnel - academic_staff_count

    # Work status
    active_count = db.query(Personnel).filter(Personnel.work_status == "ปฏิบัติงาน").count()
    on_leave_count = db.query(Personnel).filter(Personnel.work_status == "ลาศึกษาต่อ").count()

    # Academic Position distribution
    prof_count = db.query(AcademicPosition).filter(AcademicPosition.position_title == "ศาสตราจารย์").count()
    assoc_prof_count = db.query(AcademicPosition).filter(AcademicPosition.position_title == "รองศาสตราจารย์").count()
    asst_prof_count = db.query(AcademicPosition).filter(AcademicPosition.position_title == "ผู้ช่วยศาสตราจารย์").count()
    # Lecturers = Total academic minus (prof + assoc + asst)
    lecturer_count = max(0, academic_staff_count - (prof_count + assoc_prof_count + asst_prof_count))

    # Degrees distribution
    degree_counts = db.query(
        EducationHistory.degree_level, func.count(func.distinct(EducationHistory.personnel_id))
    ).group_by(EducationHistory.degree_level).all()
    degree_stats = [KeyValueStat(label=row[0], count=row[1]) for row in degree_counts]

    # Branch distribution
    branch_counts = db.query(
        Branch.name, func.count(Personnel.id)
    ).join(Personnel, Branch.id == Personnel.branch_id, isouter=True).group_by(Branch.name).all()
    branch_stats = [KeyValueStat(label=row[0], count=row[1]) for row in branch_counts if row[1] > 0]

    # Personnel Type distribution
    type_counts = db.query(
        PersonnelType.name, func.count(Personnel.id)
    ).join(Personnel, PersonnelType.id == Personnel.personnel_type_id, isouter=True).group_by(PersonnelType.name).all()
    personnel_type_stats = [KeyValueStat(label=row[0], count=row[1]) for row in type_counts]

    # Status distribution
    status_counts = db.query(
        Personnel.work_status, func.count(Personnel.id)
    ).group_by(Personnel.work_status).all()
    status_stats = [KeyValueStat(label=row[0] or "ไม่ระบุ", count=row[1]) for row in status_counts]

    return DashboardStatsResponse(
        total_personnel=total_personnel,
        academic_staff_count=academic_staff_count,
        support_staff_count=support_staff_count,
        active_count=active_count,
        on_leave_count=on_leave_count,
        prof_count=prof_count,
        assoc_prof_count=assoc_prof_count,
        asst_prof_count=asst_prof_count,
        lecturer_count=lecturer_count,
        degree_stats=degree_stats,
        branch_stats=branch_stats,
        personnel_type_stats=personnel_type_stats,
        status_stats=status_stats
    )
