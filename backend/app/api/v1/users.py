from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, RoleChecker
from app.models.user import User, Role
from app.models.personnel import Personnel
from app.schemas.auth import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash
from app.services.audit_service import log_audit

router = APIRouter(prefix="/users", tags=["User Management"], dependencies=[Depends(RoleChecker(["ADMIN"]))])

@router.get("", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    results = []
    for u in users:
        personnel = db.query(Personnel).filter(Personnel.user_id == u.id).first()
        results.append(UserResponse(
            id=u.id,
            username=u.username,
            email=u.email,
            role_id=u.role_id,
            role_name=u.role.name if u.role else None,
            is_active=u.is_active,
            personnel_id=personnel.id if personnel else None
        ))
    return results

@router.post("", response_model=UserResponse)
def create_user(
    data: UserCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="อีเมลนี้มีอยู่ในระบบแล้ว")

    new_user = User(
        username=data.username,
        email=data.email,
        password_hash=get_password_hash(data.password),
        role_id=data.role_id,
        is_active=data.is_active if data.is_active is not None else True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    log_audit(
        db=db,
        username=current_user.username,
        action="CREATE",
        module="AUTH",
        description=f"สร้างบัญชีผู้ใช้ใหม่: {new_user.username}",
        record_id=str(new_user.id),
        user_id=current_user.id,
        request=request
    )

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        role_id=new_user.role_id,
        role_name=new_user.role.name if new_user.role else None,
        is_active=new_user.is_active,
        personnel_id=None
    )

@router.put("/{id}", response_model=UserResponse)
def update_user(
    id: int,
    data: UserUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ไม่พบผู้ใช้งานนี้")

    if data.email:
        user.email = data.email
    if data.role_id:
        user.role_id = data.role_id
    if data.is_active is not None:
        user.is_active = data.is_active
    if data.password:
        user.password_hash = get_password_hash(data.password)

    db.commit()
    db.refresh(user)

    log_audit(
        db=db,
        username=current_user.username,
        action="UPDATE",
        module="AUTH",
        description=f"อัปเดตข้อมูลบัญชีผู้ใช้: {user.username}",
        record_id=str(user.id),
        user_id=current_user.id,
        request=request
    )

    personnel = db.query(Personnel).filter(Personnel.user_id == user.id).first()
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role_id=user.role_id,
        role_name=user.role.name if user.role else None,
        is_active=user.is_active,
        personnel_id=personnel.id if personnel else None
    )
