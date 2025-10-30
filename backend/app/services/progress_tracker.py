from sqlalchemy.orm import Session
from app.models.progress import Progress
from app.models.task import Task
from app.models.module import Module
from datetime import datetime

def get_or_create_progress(db: Session, user_id: int, task_id: int) -> Progress:
    progress = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.task_id == task_id
    ).first()
    
    if not progress:
        progress = Progress(user_id=user_id, task_id=task_id)
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress

def update_progress(db: Session, user_id: int, task_id: int, code: str, completed: bool):
    progress = get_or_create_progress(db, user_id, task_id)
    
    progress.attempts += 1
    progress.code_submitted = code
    
    if completed and not progress.completed:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(progress)
    return progress

def get_module_progress(db: Session, user_id: int, module_id: int):
    tasks = db.query(Task).filter(Task.module_id == module_id).all()
    task_ids = [t.id for t in tasks]
    
    completed = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.task_id.in_(task_ids),
        Progress.completed == True
    ).count()
    
    return {
        "total": len(tasks),
        "completed": completed,
        "percentage": (completed / len(tasks) * 100) if tasks else 0
    }

def get_overall_progress(db: Session, user_id: int):
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.completed == True
    ).count()
    
    total_modules = db.query(Module).count()
    
    completed_modules = 0
    modules = db.query(Module).all()
    for module in modules:
        progress = get_module_progress(db, user_id, module.id)
        if progress["percentage"] == 100:
            completed_modules += 1
    
    return {
        "total_modules": total_modules,
        "completed_modules": completed_modules,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "overall_progress": (completed_tasks / total_tasks * 100) if total_tasks else 0
    }