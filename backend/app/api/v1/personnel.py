import math
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.api.deps import get_db, get_current_user, RoleChecker
from app.models.user import User
from app.models.personnel import Personnel
from app.models.master_data import Department, Branch, Position, PersonnelType, Expertise
from app.models.academic import AcademicPosition
from app.schemas.personnel import (
    PersonnelCreate,
    PersonnelUpdate,
    PersonnelDetailResponse,
    PaginatedPersonnelResponse,
    PersonnelListItem
)
from app.services.file_service import validate_and_save_file
from app.services.audit_service import log_audit

router = APIRouter(prefix="/personnel", tags=["Personnel Management"])

def mask_citizen_id(cid: Optional[str]) -> Optional[str]:
    if not cid or len(cid) < 13:
        return cid
    # Format: 1-45XX-XXXXX-XX-X
    return f"{cid[0]}-{cid[1:3]}XX-XXXXX-{cid[10:12]}-{cid[12]}"

@router.get("", response_model=PaginatedPersonnelResponse)
def get_personnel_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    branch_id: Optional[int] = None,
    position_id: Optional[int] = None,
    personnel_type_id: Optional[int] = None,
    work_status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Personnel)

    # Role restriction: STAFF can only see their own record if requested
    user_role = current_user.role.name.upper() if current_user.role else "STAFF"
    if user_role == "STAFF":
        query = query.filter(Personnel.user_id == current_user.id)
    else:
        # Filter by search string
        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Personnel.first_name_th.like(search_pattern),
                    Personnel.last_name_th.like(search_pattern),
                    Personnel.first_name_en.like(search_pattern),
                    Personnel.last_name_en.like(search_pattern),
                    Personnel.personnel_code.like(search_pattern),
                    Personnel.email.like(search_pattern)
                )
            )
        # Filters
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

    total = query.count()
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    personnel_records = query.order_by(Personnel.id.asc()).offset((page - 1) * page_size).limit(page_size).all()

    items = []
    for p in personnel_records:
        latest_academic = db.query(AcademicPosition).filter(AcademicPosition.personnel_id == p.id).order_by(AcademicPosition.id.desc()).first()
        academic_title = latest_academic.position_title if latest_academic else None

        items.append(
            PersonnelListItem(
                id=p.id,
                personnel_code=p.personnel_code,
                prefix_th=p.prefix_th,
                first_name_th=p.first_name_th,
                last_name_th=p.last_name_th,
                full_name_th=f"{p.prefix_th}{p.first_name_th} {p.last_name_th}",
                department_name=p.department.name if p.department else None,
                branch_name=p.branch.name if p.branch else (p.department.name if p.department else None),
                position_name=p.position.name if p.position else None,
                personnel_type_name=p.personnel_type.name if p.personnel_type else None,
                academic_title=academic_title,
                email=p.email,
                phone=p.phone,
                work_status=p.work_status or "ปฏิบัติงาน",
                avatar_url=p.avatar_url
            )
        )

    return PaginatedPersonnelResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=items
    )

@router.get("/{id}", response_model=PersonnelDetailResponse)
def get_personnel_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    personnel = db.query(Personnel).filter(Personnel.id == id).first()
    if not personnel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบข้อมูลบุคลากรนี้")

    user_role = current_user.role.name.upper() if current_user.role else "STAFF"
    if user_role == "STAFF" and personnel.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ไม่มีสิทธิ์ดูข้อมูลบุคลากรท่านอื่น")

    # Mask Citizen ID for Executive or Staff viewers (Only Admin sees full raw citizen id)
    masked_cid = personnel.citizen_id
    if user_role != "ADMIN" and (user_role != "STAFF" or personnel.user_id != current_user.id):
        masked_cid = mask_citizen_id(personnel.citizen_id)

    latest_academic = db.query(AcademicPosition).filter(AcademicPosition.personnel_id == personnel.id).order_by(AcademicPosition.id.desc()).first()

    return PersonnelDetailResponse(
        id=personnel.id,
        user_id=personnel.user_id,
        personnel_code=personnel.personnel_code,
        prefix_th=personnel.prefix_th,
        first_name_th=personnel.first_name_th,
        last_name_th=personnel.last_name_th,
        full_name_th=f"{personnel.prefix_th}{personnel.first_name_th} {personnel.last_name_th}",
        prefix_en=personnel.prefix_en,
        first_name_en=personnel.first_name_en,
        last_name_en=personnel.last_name_en,
        full_name_en=f"{personnel.prefix_en or ''} {personnel.first_name_en or ''} {personnel.last_name_en or ''}".strip(),
        citizen_id=masked_cid,
        birth_date=personnel.birth_date,
        gender=personnel.gender,
        nationality=personnel.nationality,
        religion=personnel.religion,
        marital_status=personnel.marital_status,
        department_id=personnel.department_id,
        department_name=personnel.department.name if personnel.department else None,
        branch_id=personnel.branch_id,
        branch_name=personnel.branch.name if personnel.branch else None,
        position_id=personnel.position_id,
        position_name=personnel.position.name if personnel.position else None,
        personnel_type_id=personnel.personnel_type_id,
        personnel_type_name=personnel.personnel_type.name if personnel.personnel_type else None,
        academic_title=latest_academic.position_title if latest_academic else None,
        start_work_date=personnel.start_work_date,
        appoint_date=personnel.appoint_date,
        work_status=personnel.work_status,
        email=personnel.email,
        phone=personnel.phone,
        internal_phone=personnel.internal_phone,
        address=personnel.address,
        subdistrict=personnel.subdistrict,
        district=personnel.district,
        province=personnel.province,
        zipcode=personnel.zipcode,
        avatar_url=personnel.avatar_url,
        created_at=personnel.created_at,
        updated_at=personnel.updated_at,
        education_histories=personnel.education_histories,
        work_experiences=personnel.work_experiences,
        academic_positions=personnel.academic_positions,
        researches=personnel.researches,
        publications=personnel.publications,
        trainings=personnel.trainings,
        expertise_list=personnel.expertise_list
    )

@router.post("", response_model=PersonnelDetailResponse, dependencies=[Depends(RoleChecker(["ADMIN"]))])
def create_personnel(
    data: PersonnelCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check duplicate code or email
    if db.query(Personnel).filter(Personnel.personnel_code == data.personnel_code).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"รหัสบุคลากร {data.personnel_code} มีอยู่ในระบบแล้ว")
    
    if db.query(Personnel).filter(Personnel.email == data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"อีเมล {data.email} มีอยู่ในระบบแล้ว")

    personnel_data = data.model_dump(exclude={"expertise_ids"})
    new_personnel = Personnel(**personnel_data)

    if data.expertise_ids:
        expertises = db.query(Expertise).filter(Expertise.id.in_(data.expertise_ids)).all()
        new_personnel.expertise_list = expertises

    db.add(new_personnel)
    db.commit()
    db.refresh(new_personnel)

    log_audit(
        db=db,
        username=current_user.username,
        action="CREATE",
        module="PERSONNEL",
        description=f"เพิ่มข้อมูลบุคลากรใหม่: {new_personnel.prefix_th}{new_personnel.first_name_th} {new_personnel.last_name_th} ({new_personnel.personnel_code})",
        record_id=str(new_personnel.id),
        user_id=current_user.id,
        request=request
    )

    return get_personnel_by_id(new_personnel.id, current_user=current_user, db=db)

@router.put("/{id}", response_model=PersonnelDetailResponse)
def update_personnel(
    id: int,
    data: PersonnelUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    personnel = db.query(Personnel).filter(Personnel.id == id).first()
    if not personnel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบข้อมูลบุคลากรนี้")

    user_role = current_user.role.name.upper() if current_user.role else "STAFF"
    if user_role == "STAFF" and personnel.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ไม่มีสิทธิ์แก้ไขข้อมูลบุคลากรท่านอื่น")

    # Update allowed fields
    update_dict = data.model_dump(exclude_unset=True)
    expertise_ids = update_dict.pop("expertise_ids", None)

    for field, value in update_dict.items():
        # If staff, prevent changing position, code, or personnel type
        if user_role == "STAFF" and field in ["department_id", "branch_id", "position_id", "personnel_type_id", "work_status"]:
            continue
        setattr(personnel, field, value)

    if expertise_ids is not None:
        expertises = db.query(Expertise).filter(Expertise.id.in_(expertise_ids)).all()
        personnel.expertise_list = expertises

    db.commit()
    db.refresh(personnel)

    log_audit(
        db=db,
        username=current_user.username,
        action="UPDATE",
        module="PERSONNEL",
        description=f"แก้ไขข้อมูลบุคลากร: {personnel.prefix_th}{personnel.first_name_th} {personnel.last_name_th} ({personnel.personnel_code})",
        record_id=str(personnel.id),
        user_id=current_user.id,
        request=request
    )

    return get_personnel_by_id(personnel.id, current_user=current_user, db=db)

@router.delete("/{id}", dependencies=[Depends(RoleChecker(["ADMIN"]))])
def delete_personnel(
    id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    personnel = db.query(Personnel).filter(Personnel.id == id).first()
    if not personnel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบข้อมูลบุคลากรนี้")

    code = personnel.personnel_code
    name = f"{personnel.prefix_th}{personnel.first_name_th} {personnel.last_name_th}"

    db.delete(personnel)
    db.commit()

    log_audit(
        db=db,
        username=current_user.username,
        action="DELETE",
        module="PERSONNEL",
        description=f"ลบข้อมูลบุคลากร: {name} (รหัส: {code})",
        record_id=str(id),
        user_id=current_user.id,
        request=request
    )

    return {"message": f"ลบข้อมูลบุคลากร {name} สำเร็จเรียบร้อยแล้ว"}

@router.post("/{id}/avatar")
def upload_avatar(
    id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    personnel = db.query(Personnel).filter(Personnel.id == id).first()
    if not personnel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบข้อมูลบุคลากร")

    user_role = current_user.role.name.upper() if current_user.role else "STAFF"
    if user_role == "STAFF" and personnel.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ไม่มีสิทธิ์อัปโหลดรูปภาพให้ผู้อื่น")

    avatar_path = validate_and_save_file(file, subfolder="avatars")
    personnel.avatar_url = avatar_path
    db.commit()

    return {"avatar_url": avatar_path, "message": "อัปโหลดรูปภาพประจำตัวสำเร็จ"}
