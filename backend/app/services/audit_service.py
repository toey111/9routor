from fastapi import Request
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from typing import Optional

def log_audit(
    db: Session,
    username: str,
    action: str,
    module: str,
    description: str,
    record_id: Optional[str] = None,
    user_id: Optional[int] = None,
    request: Optional[Request] = None
):
    ip = "127.0.0.1"
    user_agent = "Unknown"
    if request:
        client = request.client
        if client:
            ip = client.host
        user_agent = request.headers.get("user-agent", "Unknown")[:250]
        
    audit_entry = AuditLog(
        user_id=user_id,
        username=username,
        action=action,
        module=module,
        record_id=str(record_id) if record_id else None,
        ip_address=ip,
        user_agent=user_agent,
        description=description
    )
    db.add(audit_entry)
    db.commit()
