from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

class KeyValueStat(BaseModel):
    label: str
    count: int

class DashboardStatsResponse(BaseModel):
    total_personnel: int
    academic_staff_count: int
    support_staff_count: int
    active_count: int
    on_leave_count: int
    prof_count: int       # ศาสตราจารย์
    assoc_prof_count: int # รองศาสตราจารย์
    asst_prof_count: int  # ผู้ช่วยศาสตราจารย์
    lecturer_count: int   # อาจารย์
    degree_stats: List[KeyValueStat]
    branch_stats: List[KeyValueStat]
    personnel_type_stats: List[KeyValueStat]
    status_stats: List[KeyValueStat]

class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    username: str
    action: str
    module: str
    record_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedAuditLogResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[AuditLogResponse]
