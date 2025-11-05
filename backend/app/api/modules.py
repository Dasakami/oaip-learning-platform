from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.module import Module
from app.models.user import User
from app.schemas.module import Module as ModuleSchema, ModuleWithProgress
from app.services.auth import get_current_user
from app.services.progress_tracker import get_module_progress

router = APIRouter()

@router.get("/", response_model=List[ModuleWithProgress])
def get_modules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    modules = db.query(Module).order_by(Module.order).all()
    
    result = []
    for module in modules:
        progress = get_module_progress(db, current_user.id, module.id)
        module_dict = {
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "order": module.order,
            "content": module.content,
            "completed_tasks": progress["completed"],
            "total_tasks": progress["total"],
            "progress_percentage": progress["percentage"]
        }
        result.append(module_dict)
    
    return result

@router.get("/{module_id}", response_model=ModuleSchema)
def get_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module