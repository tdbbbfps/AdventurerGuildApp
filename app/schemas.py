from pydantic import BaseModel, Field

class AdventurerBase(BaseModel):
    name : str = Field(..., min_length=3, max_length=50, description="adventurer's name.")
    class_id : int = Field(..., description="adventurer's class.")
    level : int = Field(..., description="adventurer's level.", ge=1)
    is_active : bool = Field(description="adventurer's status.", default=True)
    gold : int = Field(ge=0, description="adventurer's gold.", default=0)

class AdventurerCreate(AdventurerBase):
    pass

class Adventurer(AdventurerBase):
    id : int

    class Config:
        from_attributes = True
        
class ClassBase(BaseModel):
    name : str = Field(..., min_length=3, max_length=50, description="class's name.")

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    id : int

    class Config:
        from_attributes = True