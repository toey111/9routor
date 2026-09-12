from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, RoleChecker
from app.models.user import User
from app.models.master_data import Department, Branch, Position, PersonnelType, Expertise
from app.schemas.master_data import (
    DepartmentCreate, DepartmentResponse,
    BranchCreate, BranchResponse,
    PositionCreate, PositionResponse,
    PersonnelTypeCreate, PersonnelTypeResponse,
    ExpertiseCreate, ExpertiseResponse
)
from app.services.audit_service import log_audit

router = APIRouter(tags=["Master Data"])

# --- Departments ---
@router.get("/departments", response_model=List[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.post("/departments", response_model=DepartmentResponse, dependencies=[Depends(RoleChecker(["ADMIN"]))])
def create_department(data: DepartmentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    dept = Department(**data.model_dump())
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept

# --- Branches ---
@router.get("/branches", response_model=List[BranchResponse])
def get_branches(department_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Branch)
    if department_id:
        query = query.filter(Branch.department_id == department_id)
    branches = query.all()
    results = []
    for b in branches:
        results.append(BranchResponse(
            id=b.id,
            department_id=b.department_id,
            name=b.name,
            code=b.code,
            department_name=b.department.name if b.department else None
        ))
    return results

@router.post("/branches", response_model=BranchResponse, dependencies=[Depends(RoleChecker(["ADMIN"]))])
def create_branch(data: BranchCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    branch = Branch(**data.model_dump())
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return BranchResponse(
        id=branch.id,
        department_id=branch.department_id,
        name=branch.name,
        code=branch.code,
        department_name=branch.department.name if branch.department else None
    )

# --- Positions ---
@router.get("/positions", response_model=List[PositionResponse])
def get_positions(db: Session = Depends(get_db)):
    return db.query(Position).all()

@router.post("/positions", response_model=PositionResponse, dependencies=[Depends(RoleChecker(["ADMIN"]))])
def create_position(data: PositionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    pos = Position(**data.model_dump())
    db.add(pos)
    db.commit()
    db.refresh(pos)
    return pos

# --- Personnel Types ---
@router.get("/personnel-types", response_model=List[PersonnelTypeResponse])
def get_personnel_types(db: Session = Depends(get_db)):
    return db.query(PersonnelType).all()

@router.post("/personnel-types", response_model=PersonnelTypeResponse, dependencies=[Depends(RoleChecker(["ADMIN"]))])
def create_personnel_type(data: PersonnelTypeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    pt = PersonnelType(**data.model_dump())
    db.add(pt)
    db.commit()
    db.refresh(pt)
    return pt

# --- Expertise List ---
@router.get("/expertise", response_model=List[ExpertiseResponse])
def get_expertise_list(db: Session = Depends(get_db)):
    return db.query(Expertise).all()

@router.post("/expertise", response_model=ExpertiseResponse, dependencies=[Depends(RoleChecker(["ADMIN"]))])
def create_expertise(data: ExpertiseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    exp = Expertise(**data.model_dump())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp
