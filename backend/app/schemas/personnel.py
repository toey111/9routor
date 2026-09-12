from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, EmailStr
from app.schemas.academic import (
    EducationResponse,
    WorkExperienceResponse,
    AcademicPositionResponse,
    ResearchResponse,
    PublicationResponse,
    TrainingResponse
)
from app.schemas.master_data import ExpertiseResponse

class PersonnelBase(BaseModel):
    personnel_code: str
    prefix_th: str
    first_name_th: str
    last_name_th: str
    prefix_en: Optional[str] = None
    first_name_en: Optional[str] = None
    last_name_en: Optional[str] = None
    citizen_id: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = "ชาย"
    nationality: Optional[str] = "ไทย"
    religion: Optional[str] = "พุทธ"
    marital_status: Optional[str] = "โสด"
    department_id: int
    branch_id: Optional[int] = None
    position_id: int
    personnel_type_id: int
    start_work_date: Optional[date] = None
    appoint_date: Optional[date] = None
    work_status: Optional[str] = "ปฏิบัติงาน"
    email: EmailStr
    phone: Optional[str] = None
    internal_phone: Optional[str] = None
    address: Optional[str] = None
    subdistrict: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    zipcode: Optional[str] = None
    avatar_url: Optional[str] = None

class PersonnelCreate(PersonnelBase):
    user_id: Optional[int] = None
    expertise_ids: Optional[List[int]] = []

class PersonnelUpdate(BaseModel):
    prefix_th: Optional[str] = None
    first_name_th: Optional[str] = None
    last_name_th: Optional[str] = None
    prefix_en: Optional[str] = None
    first_name_en: Optional[str] = None
    last_name_en: Optional[str] = None
    citizen_id: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    marital_status: Optional[str] = None
    department_id: Optional[int] = None
    branch_id: Optional[int] = None
    position_id: Optional[int] = None
    personnel_type_id: Optional[int] = None
    start_work_date: Optional[date] = None
    appoint_date: Optional[date] = None
    work_status: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    internal_phone: Optional[str] = None
    address: Optional[str] = None
    subdistrict: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    zipcode: Optional[str] = None
    avatar_url: Optional[str] = None
    expertise_ids: Optional[List[int]] = None

class PersonnelListItem(BaseModel):
    id: int
    personnel_code: str
    prefix_th: str
    first_name_th: str
    last_name_th: str
    full_name_th: Optional[str] = None
    department_name: Optional[str] = None
    branch_name: Optional[str] = None
    position_name: Optional[str] = None
    personnel_type_name: Optional[str] = None
    academic_title: Optional[str] = None
    email: str
    phone: Optional[str] = None
    work_status: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

class PersonnelDetailResponse(PersonnelBase):
    id: int
    user_id: Optional[int] = None
    full_name_th: Optional[str] = None
    full_name_en: Optional[str] = None
    department_name: Optional[str] = None
    branch_name: Optional[str] = None
    position_name: Optional[str] = None
    personnel_type_name: Optional[str] = None
    academic_title: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    education_histories: List[EducationResponse] = []
    work_experiences: List[WorkExperienceResponse] = []
    academic_positions: List[AcademicPositionResponse] = []
    researches: List[ResearchResponse] = []
    publications: List[PublicationResponse] = []
    trainings: List[TrainingResponse] = []
    expertise_list: List[ExpertiseResponse] = []

    class Config:
        from_attributes = True

class PaginatedPersonnelResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[PersonnelListItem]
