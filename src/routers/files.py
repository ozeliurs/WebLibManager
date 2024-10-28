from fastapi import APIRouter
from sqlmodel import select

from ..models import File
from ..database import SessionDep

router = APIRouter()

@router.get("/files/")
def read_files(session: SessionDep, offset: int = 0, limit: int = 100):
    files = session.exec(select(File).offset(offset).limit(limit)).all()
    return files
