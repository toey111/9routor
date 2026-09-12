from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, RoleChecker
from app.models.user import User
from app.models.personnel import Personnel
from app.models.academic import (
    EducationHistory,
    WorkExperience,
    AcademicPosition,
    Research,
    Publication,
    Training
)
from app.schemas.academic import (
    EducationCreate, EducationResponse,
    WorkExperienceCreate, WorkExperienceResponse,
    AcademicPositionCreate, AcademicPositionResponse,
    ResearchCreate, ResearchResponse,
    PublicationCreate, PublicationResponse,
    TrainingCreate, TrainingResponse
)
from app.services.audit_service import log_audit

router = APIRouter(tags=["Academic & Profile Sub-resources"])

def verify_personnel_access(personnel_id: int, current_user: User, db: Session):
    personnel = db.query(Personnel).filter(Personnel.id == personnel_id).first()
    if not personnel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบข้อมูลบุคลากร")
    
    role = current_user.role.name.upper() if current_user.role else "STAFF"
    if role == "STAFF" and personnel.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ไม่มีสิทธิ์จัดการข้อมูลของบุคลากรท่านอื่น")
    return personnel

# --- Education Histories ---
@router.post("/personnel/{id}/education", response_model=EducationResponse)
def add_education(
    id: int,
    data: EducationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_personnel_access(id, current_user, db)
    edu = EducationHistory(personnel_id=id, **data.model_dump())
    db.add(edu)
    db.commit()
    db.refresh(edu)
    return edu

@router.delete("/education/{id}")
def delete_education(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    edu = db.query(EducationHistory).filter(EducationHistory.id == id).first()
    if not edu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบรายการการศึกษานี้")
    verify_personnel_access(edu.personnel_id, current_user, db)
    db.delete(edu)
    db.commit()
    return {"message": "ลบประวัติการศึกษาเรียบร้อยแล้ว"}

# --- Work Experiences ---
@router.post("/personnel/{id}/work-experience", response_model=WorkExperienceResponse)
def add_work_experience(
    id: int,
    data: WorkExperienceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_personnel_access(id, current_user, db)
    work = WorkExperience(personnel_id=id, **data.model_dump())
    db.add(work)
    db.commit()
    db.refresh(work)
    return work

@router.delete("/work-experience/{id}")
def delete_work_experience(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    work = db.query(WorkExperience).filter(WorkExperience.id == id).first()
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบรายการประวัติการทำงาน")
    verify_personnel_access(work.personnel_id, current_user, db)
    db.delete(work)
    db.commit()
    return {"message": "ลบประวัติการทำงานเรียบร้อยแล้ว"}

# --- Academic Positions ---
@router.post("/personnel/{id}/academic-position", response_model=AcademicPositionResponse)
def add_academic_position(
    id: int,
    data: AcademicPositionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_personnel_access(id, current_user, db)
    acad = AcademicPosition(personnel_id=id, **data.model_dump())
    db.add(acad)
    db.commit()
    db.refresh(acad)
    return acad

@router.delete("/academic-position/{id}")
def delete_academic_position(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    acad = db.query(AcademicPosition).filter(AcademicPosition.id == id).first()
    if not acad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบรายการตำแหน่งทางวิชาการ")
    verify_personnel_access(acad.personnel_id, current_user, db)
    db.delete(acad)
    db.commit()
    return {"message": "ลบตำแหน่งทางวิชาการเรียบร้อยแล้ว"}

# --- Research ---
@router.post("/personnel/{id}/research", response_model=ResearchResponse)
def add_research(
    id: int,
    data: ResearchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_personnel_access(id, current_user, db)
    res = Research(personnel_id=id, **data.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

@router.delete("/research/{id}")
def delete_research(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    res = db.query(Research).filter(Research.id == id).first()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบผลงานวิจัย")
    verify_personnel_access(res.personnel_id, current_user, db)
    db.delete(res)
    db.commit()
    return {"message": "ลบผลงานวิจัยเรียบร้อยแล้ว"}

# --- Publications ---
@router.post("/personnel/{id}/publications", response_model=PublicationResponse)
def add_publication(
    id: int,
    data: PublicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_personnel_access(id, current_user, db)
    pub = Publication(personnel_id=id, **data.model_dump())
    db.add(pub)
    db.commit()
    db.refresh(pub)
    return pub

@router.delete("/publications/{id}")
def delete_publication(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pub = db.query(Publication).filter(Publication.id == id).first()
    if not pub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบผลงานตีพิมพ์")
    verify_personnel_access(pub.personnel_id, current_user, db)
    db.delete(pub)
    db.commit()
    return {"message": "ลบผลงานตีพิมพ์เรียบร้อยแล้ว"}

# --- Trainings ---
@router.post("/personnel/{id}/trainings", response_model=TrainingResponse)
def add_training(
    id: int,
    data: TrainingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_personnel_access(id, current_user, db)
    train = Training(personnel_id=id, **data.model_dump())
    db.add(train)
    db.commit()
    db.refresh(train)
    return train

@router.delete("/trainings/{id}")
def delete_training(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    train = db.query(Training).filter(Training.id == id).first()
    if not train:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบประวัติการอบรม")
    verify_personnel_access(train.personnel_id, current_user, db)
    db.delete(train)
    db.commit()
    return {"message": "ลบประวัติการอบรมเรียบร้อยแล้ว"}
