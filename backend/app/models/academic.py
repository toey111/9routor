from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class EducationHistory(Base):
    __tablename__ = "education_histories"

    id = Column(Integer, primary_key=True, index=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False)
    degree_level = Column(String(50), nullable=False) # ปวส., ปริญญาตรี, ปริญญาโท, ปริญญาเอก
    degree_name = Column(String(150), nullable=False)
    field_of_study = Column(String(150), nullable=False)
    institution = Column(String(200), nullable=False)
    country = Column(String(100), default="ไทย")
    graduation_year = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())

    personnel = relationship("Personnel", back_populates="education_histories")

class WorkExperience(Base):
    __tablename__ = "work_experiences"

    id = Column(Integer, primary_key=True, index=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False)
    organization = Column(String(200), nullable=False)
    position = Column(String(150), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())

    personnel = relationship("Personnel", back_populates="work_experiences")

class AcademicPosition(Base):
    __tablename__ = "academic_positions"

    id = Column(Integer, primary_key=True, index=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False)
    position_title = Column(String(100), nullable=False) # อาจารย์, ผู้ช่วยศาสตราจารย์, รองศาสตราจารย์, ศาสตราจารย์
    appointed_date = Column(Date, nullable=True)
    order_number = Column(String(100), nullable=True)
    document_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())

    personnel = relationship("Personnel", back_populates="academic_positions")

class Research(Base):
    __tablename__ = "researches"

    id = Column(Integer, primary_key=True, index=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(300), nullable=False)
    research_type = Column(String(100), default="งานวิจัยประยุกต์")
    year = Column(Integer, nullable=False)
    funding_source = Column(String(200), nullable=True)
    budget = Column(Numeric(12, 2), default=0.00)
    doi = Column(String(150), nullable=True)
    url = Column(String(255), nullable=True)
    abstract_detail = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())

    personnel = relationship("Personnel", back_populates="researches")

class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False)
    article_title = Column(String(300), nullable=False)
    authors = Column(String(300), nullable=False)
    journal_conference_name = Column(String(250), nullable=False)
    publication_year = Column(Integer, nullable=False)
    volume = Column(String(50), nullable=True)
    issue = Column(String(50), nullable=True)
    pages = Column(String(50), nullable=True)
    doi = Column(String(150), nullable=True)
    url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())

    personnel = relationship("Personnel", back_populates="publications")

class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False)
    course_name = Column(String(250), nullable=False)
    organizer = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    hours = Column(Integer, default=0)
    location = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())

    personnel = relationship("Personnel", back_populates="trainings")
