from sqlmodel import Session

from .fs_scan import fs_scan
from .ffprobe_scan import ffprobe_scan

from ..models import Job
from ..database import engine

def update_job_status(status: str, job_id: int) -> None:
    with Session(engine) as session:
        if job := session.get(Job, job_id):
            job.status = status
            session.add(job)
            session.commit()
        else:
            raise ValueError(f"Job {job_id} not found")

def full_scan(path: str, job_id: int) -> None:
    try:
        update_job_status("scanning files", job_id)
        fs_scan(path)

        update_job_status("scanning files metadata", job_id)
        ffprobe_scan(job_id)

        update_job_status("completed", job_id)

    except Exception as e:
        print(e)
        update_job_status(f"failed - {e}", job_id)
        return
