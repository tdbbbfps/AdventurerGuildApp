from pydantic import BaseModel, Field

class AdventurerBase(BaseModel):
    name : str = Field(..., min_length=3, max_length=50, description="adventurer's name.")
    job_id : int = Field(..., description="adventurer's job.")
    level : int = Field(..., description="adventurer's level.", ge=1)
    is_active : bool = Field(description="adventurer's status.", default=True)
    gold : int = Field(description="adventurer's gold.", ge=0, default=0)

class AdventurerCreate(AdventurerBase):
    pass

class AdventurerUpdate(BaseModel):
    id : int = Field(..., description="Adventurer's ID.")
    name : str = Field(description="Adventurer's new name", min_length=3, max_length=50, nullable=True)
    job_id : int = Field(description="Adventurer's new job.", nullable=True)
    level : int = Field(description="Adventurer's new level.", ge=1, nullable=True)
    is_active : bool = Field(description="Adventurer's new status.", nullable=True)
    gold : int = Field(description="Adventurer's new gold.", ge=0, nullable=True)

class Job(BaseModel):
    name : str = Field(..., min_length=3, max_length=50, description="Job's name.")

class JobCreate(Job):
    pass

class Adventurer(AdventurerBase):
    id : int
    job : Job
    class Config:
        from_attributes = True
