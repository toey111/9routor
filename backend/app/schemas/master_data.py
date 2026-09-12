from typing import Optional
from pydantic import BaseModel

class DepartmentBase(BaseModel):
    name: str
    code: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int
    class Config:
        from_attributes = True

class BranchBase(BaseModel):
    department_id: int
    name: str
    code: Optional[str] = None

class BranchCreate(BranchBase):
    pass

class BranchResponse(BranchBase):
    id: int
    department_name: Optional[str] = None
    class Config:
        from_attributes = True

class PositionBase(BaseModel):
    name: str

class PositionCreate(PositionBase):
    pass

class PositionResponse(PositionBase):
    id: int
    class Config:
        from_attributes = True

class PersonnelTypeBase(BaseModel):
    name: str

class PersonnelTypeCreate(PersonnelTypeBase):
    pass

class PersonnelTypeResponse(PersonnelTypeBase):
    id: int
    class Config:
        from_attributes = True

class ExpertiseBase(BaseModel):
    name: str

class ExpertiseCreate(ExpertiseBase):
    pass

class ExpertiseResponse(ExpertiseBase):
    id: int
    class Config:
        from_attributes = True
