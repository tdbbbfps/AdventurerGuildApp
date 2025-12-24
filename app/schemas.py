from pydantic import BaseModel, Field

class AdventurerBase(BaseModel):
    name : str = Field(..., min_length=3, max_length=50, description="adventurer's name.")
    job_id : int = Field(..., description="adventurer's job.")
    level : int = Field(..., description="adventurer's level.", ge=1)
    is_active : bool = Field(description="adventurer's status.", default=True)
    gold : int = Field(ge=0, description="adventurer's gold.", default=0)

class AdventurerCreate(AdventurerBase):
    pass
        
class JobBase(BaseModel):
    name : str = Field(..., min_length=3, max_length=50, description="Job's name.")

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id : int

    class Config:
        from_attributes = True

class Adventurer(AdventurerBase):
    id : int
    job : Job
    class Config:
        from_attributes = True
