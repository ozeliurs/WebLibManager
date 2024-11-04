from fastapi import APIRouter, BackgroundTasks
from sqlmodel import select

from ..jobs.full_scan import full_scan
from ..models import Job
from ..database import SessionDep

router = APIRouter()

@router.get("/scans/")
def read_scans(session: SessionDep, offset: int = 0, limit: int = 100):
    scans = session.exec(select(Job).offset(offset).limit(limit)).all()
    return scans


@router.post("/scans/")
def create_scan(path: str, background_tasks: BackgroundTasks, session: SessionDep):
    job = Job(status="pending")
    session.add(job)
    session.commit()
    session.refresh(job)

    background_tasks.add_task(full_scan, path, job.id)
    return job
