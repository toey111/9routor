from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
from app.api.deps import get_db, get_current_user
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.models.personnel import Personnel
from app.schemas.auth import Token, LoginRequest, UserResponse, ChangePasswordRequest
from app.services.audit_service import log_audit

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.username == login_data.username) | (User.email == login_data.username)
    ).first()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="บัญชีผู้ใช้งานนี้ถูกระงับการใช้งาน กรุณาติดต่อผู้ดูแลระบบ"
        )

    user.last_login = datetime.utcnow()
    db.commit()

    role_name = user.role.name.upper() if user.role else "STAFF"
    access_token = create_access_token(subject=user.username, role=role_name)

    personnel = db.query(Personnel).filter(Personnel.user_id == user.id).first()
    personnel_id = personnel.id if personnel else None
    full_name = f"{personnel.prefix_th}{personnel.first_name_th} {personnel.last_name_th}" if personnel else user.username

    log_audit(
        db=db,
        username=user.username,
        action="LOGIN",
        module="AUTH",
        description=f"ผู้ใช้งาน {user.username} (Role: {role_name}) เข้าสู่ระบบสำเร็จ",
        record_id=str(user.id),
        user_id=user.id,
        request=request
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role_name,
        "user_id": user.id,
        "username": user.username,
        "personnel_id": personnel_id,
        "full_name": full_name
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    personnel = db.query(Personnel).filter(Personnel.user_id == current_user.id).first()
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.name if current_user.role else "STAFF",
        "is_active": current_user.is_active,
        "personnel_id": personnel.id if personnel else None,
        "full_name": f"{personnel.prefix_th}{personnel.first_name_th} {personnel.last_name_th}" if personnel else current_user.username,
        "avatar_url": personnel.avatar_url if personnel else None
    }

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="รหัสผ่านปัจจุบันไม่ถูกต้อง"
        )
    
    if len(data.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="รหัสผ่านใหม่ต้องมีความยาวอย่างน้อย 6 ตัวอักษร"
        )

    current_user.password_hash = get_password_hash(data.new_password)
    db.commit()

    log_audit(
        db=db,
        username=current_user.username,
        action="UPDATE",
        module="AUTH",
        description=f"ผู้ใช้งาน {current_user.username} เปลี่ยนรหัสผ่านสำเร็จ",
        record_id=str(current_user.id),
        user_id=current_user.id
    )

    return {"message": "เปลี่ยนรหัสผ่านสำเร็จเรียบร้อยแล้ว"}
