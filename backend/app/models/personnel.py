from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from app.core.database import Base

personnel_expertise = Table(
    "personnel_expertise",
    Base.metadata,
    Column("personnel_id", Integer, ForeignKey("personnel.id", ondelete="CASCADE"), primary_key=True),
    Column("expertise_id", Integer, ForeignKey("expertise.id", ondelete="CASCADE"), primary_key=True)
)

class Personnel(Base):
    __tablename__ = "personnel"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)
    personnel_code = Column(String(50), unique=True, nullable=False, index=True)
    prefix_th = Column(String(50), nullable=False)
    first_name_th = Column(String(100), nullable=False, index=True)
    last_name_th = Column(String(100), nullable=False, index=True)
    prefix_en = Column(String(50), nullable=True)
    first_name_en = Column(String(100), nullable=True)
    last_name_en = Column(String(100), nullable=True)
    citizen_id = Column(String(50), nullable=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(String(20), default="ชาย")
    nationality = Column(String(50), default="ไทย")
    religion = Column(String(50), default="พุทธ")
    marital_status = Column(String(50), default="โสด")

    department_id = Column(Integer, ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="SET NULL"), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="RESTRICT"), nullable=False)
    personnel_type_id = Column(Integer, ForeignKey("personnel_types.id", ondelete="RESTRICT"), nullable=False)

    start_work_date = Column(Date, nullable=True)
    appoint_date = Column(Date, nullable=True)
    work_status = Column(String(50), default="ปฏิบัติงาน", index=True)

    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    internal_phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    subdistrict = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    province = Column(String(100), nullable=True)
    zipcode = Column(String(20), nullable=True)
    avatar_url = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="personnel")
    department = relationship("Department", back_populates="personnel")
    branch = relationship("Branch", back_populates="personnel")
    position = relationship("Position", back_populates="personnel")
    personnel_type = relationship("PersonnelType", back_populates="personnel")

    education_histories = relationship("EducationHistory", back_populates="personnel", cascade="all, delete-orphan")
    work_experiences = relationship("WorkExperience", back_populates="personnel", cascade="all, delete-orphan")
    academic_positions = relationship("AcademicPosition", back_populates="personnel", cascade="all, delete-orphan")
    researches = relationship("Research", back_populates="personnel", cascade="all, delete-orphan")
    publications = relationship("Publication", back_populates="personnel", cascade="all, delete-orphan")
    trainings = relationship("Training", back_populates="personnel", cascade="all, delete-orphan")
    expertise_list = relationship("Expertise", secondary=personnel_expertise, back_populates="personnel")
    files = relationship("UploadedFile", back_populates="personnel", cascade="all, delete-orphan")
