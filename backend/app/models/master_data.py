from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    code = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now())

    branches = relationship("Branch", back_populates="department", cascade="all, delete-orphan")
    personnel = relationship("Personnel", back_populates="department")

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    code = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now())

    department = relationship("Department", back_populates="branches")
    personnel = relationship("Personnel", back_populates="branch")

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

    personnel = relationship("Personnel", back_populates="position")

class PersonnelType(Base):
    __tablename__ = "personnel_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

    personnel = relationship("Personnel", back_populates="personnel_type")

class Expertise(Base):
    __tablename__ = "expertise"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

    personnel = relationship("Personnel", secondary="personnel_expertise", back_populates="expertise_list")
