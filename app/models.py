from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Adventurer(Base):
    __tablename__ = "adventurers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    gold = Column(Integer, default=0)
    
    classes = relationship("Class", back_populates="adventurers")
    
class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    
    adventurers = relationship("Adventurer", back_populates="class")