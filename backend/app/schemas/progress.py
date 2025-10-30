from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProgressBase(BaseModel):
    user_id: int
    task_id: int
    completed: bool = False

class ProgressCreate(ProgressBase):
    code_submitted: Optional[str] = None

class Progress(ProgressBase):
    id: int
    code_submitted: Optional[str]
    completed_at: Optional[datetime]
    attempts: int
    
    class Config:
        from_attributes = True

class ProgressStats(BaseModel):
    total_modules: int
    completed_modules: int
    total_tasks: int
    completed_tasks: int
    overall_progress: float