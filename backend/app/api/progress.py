from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.progress import ProgressStats
from app.services.auth import get_current_user
from app.services.progress_tracker import get_overall_progress

router = APIRouter()

@router.get("/stats", response_model=ProgressStats)
def get_progress_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить общую статистику прогресса"""
    return get_overall_progress(db, current_user.id)