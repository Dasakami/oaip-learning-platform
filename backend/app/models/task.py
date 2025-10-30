from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    title = Column(String)
    description = Column(Text)
    difficulty = Column(String)
    starter_code = Column(Text, nullable=True)
    test_cases = Column(JSON)
    order = Column(Integer)
    
    module = relationship("Module", back_populates="tasks")