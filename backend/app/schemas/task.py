from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TestCase(BaseModel):
    input: str
    expected_output: str

class TaskBase(BaseModel):
    module_id: int
    title: str
    description: str
    difficulty: str
    starter_code: Optional[str] = None
    test_cases: List[Dict[str, Any]]
    order: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    
    class Config:
        from_attributes = True

class TaskWithProgress(Task):
    completed: bool = False
    attempts: int = 0

class CodeSubmission(BaseModel):
    task_id: int
    code: str

class CodeResult(BaseModel):
    success: bool
    message: str
    test_results: List[Dict[str, Any]]