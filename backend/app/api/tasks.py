from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.models.progress import Progress
from app.schemas.task import Task as TaskSchema, TaskWithProgress, CodeSubmission, CodeResult
from app.services.auth import get_current_user
from app.services.code_checker import check_code
from app.services.progress_tracker import update_progress

router = APIRouter()

@router.get("/module/{module_id}", response_model=List[TaskWithProgress])
def get_module_tasks(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.module_id == module_id).order_by(Task.order).all()
    
    result = []
    for task in tasks:
        progress = db.query(Progress).filter(
            Progress.user_id == current_user.id,
            Progress.task_id == task.id
        ).first()
        
        task_dict = {
            "id": task.id,
            "module_id": task.module_id,
            "title": task.title,
            "description": task.description,
            "difficulty": task.difficulty,
            "starter_code": task.starter_code,
            "test_cases": task.test_cases,
            "order": task.order,
            "completed": progress.completed if progress else False,
            "attempts": progress.attempts if progress else 0
        }
        result.append(task_dict)
    
    return result

@router.get("/{task_id}", response_model=TaskWithProgress)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.task_id == task.id
    ).first()
    
    return {
        "id": task.id,
        "module_id": task.module_id,
        "title": task.title,
        "description": task.description,
        "difficulty": task.difficulty,
        "starter_code": task.starter_code,
        "test_cases": task.test_cases,
        "order": task.order,
        "completed": progress.completed if progress else False,
        "attempts": progress.attempts if progress else 0
    }

@router.post("/submit", response_model=CodeResult)
def submit_code(
    submission: CodeSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == submission.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    result = check_code(submission.code, task.test_cases)

    update_progress(db, current_user.id, task.id, submission.code, result["success"])
    
    return result