from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Adventurer(Base):
    __tablename__ = "adventurers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    gold = Column(Integer, default=0)
    # Add relationship
    job = relationship("Job", back_populates="adventurers")
    
class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True, unique=True)
    # Add relationship
    adventurers = relationship("Adventurer", back_populates="job")