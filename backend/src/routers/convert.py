from fastapi import APIRouter, BackgroundTasks
from sqlmodel import select

from ..jobs.media_convert import media_convert
from ..models import Job
from ..database import SessionDep

router = APIRouter()

@router.get("/converts/")
def read_converts(session: SessionDep, offset: int = 0, limit: int = 100):
    """Get list of conversion jobs"""
    converts = session.exec(select(Job).offset(offset).limit(limit)).all()
    return converts

@router.post("/converts/")
def create_convert(file_path: str, background_tasks: BackgroundTasks, session: SessionDep):
    """Start a new conversion job"""
    job = Job(status="pending")
    session.add(job)
    session.commit()
    session.refresh(job)

    background_tasks.add_task(media_convert, file_path, job.id)
    return job
