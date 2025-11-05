from pydantic import BaseModel

class ModuleBase(BaseModel):
    title: str
    description: str
    order: int
    content: str

class ModuleCreate(ModuleBase):
    pass

class Module(ModuleBase):
    id: int
    
    class Config:
        from_attributes = True

class ModuleWithProgress(Module):
    completed_tasks: int = 0
    total_tasks: int = 0
    progress_percentage: float = 0.0