from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import BaseModel

# Education
class EducationBase(BaseModel):
    degree_level: str
    degree_name: str
    field_of_study: str
    institution: str
    country: Optional[str] = "ไทย"
    graduation_year: int

class EducationCreate(EducationBase):
    pass

class EducationResponse(EducationBase):
    id: int
    personnel_id: int
    class Config:
        from_attributes = True

# Work Experience
class WorkExperienceBase(BaseModel):
    organization: str
    position: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

class WorkExperienceCreate(WorkExperienceBase):
    pass

class WorkExperienceResponse(WorkExperienceBase):
    id: int
    personnel_id: int
    class Config:
        from_attributes = True

# Academic Position
class AcademicPositionBase(BaseModel):
    position_title: str
    appointed_date: Optional[date] = None
    order_number: Optional[str] = None
    document_path: Optional[str] = None

class AcademicPositionCreate(AcademicPositionBase):
    pass

class AcademicPositionResponse(AcademicPositionBase):
    id: int
    personnel_id: int
    class Config:
        from_attributes = True

# Research
class ResearchBase(BaseModel):
    title: str
    research_type: Optional[str] = "งานวิจัยประยุกต์"
    year: int
    funding_source: Optional[str] = None
    budget: Optional[Decimal] = Decimal("0.00")
    doi: Optional[str] = None
    url: Optional[str] = None
    abstract_detail: Optional[str] = None

class ResearchCreate(ResearchBase):
    pass

class ResearchResponse(ResearchBase):
    id: int
    personnel_id: int
    class Config:
        from_attributes = True

# Publication
class PublicationBase(BaseModel):
    article_title: str
    authors: str
    journal_conference_name: str
    publication_year: int
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None

class PublicationCreate(PublicationBase):
    pass

class PublicationResponse(PublicationBase):
    id: int
    personnel_id: int
    class Config:
        from_attributes = True

# Training
class TrainingBase(BaseModel):
    course_name: str
    organizer: str
    start_date: date
    end_date: date
    hours: Optional[int] = 0
    location: Optional[str] = None
    description: Optional[str] = None

class TrainingCreate(TrainingBase):
    pass

class TrainingResponse(TrainingBase):
    id: int
    personnel_id: int
    class Config:
        from_attributes = True
