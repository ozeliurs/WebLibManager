from fastapi import APIRouter

from ..jobs.fs_scan import fs_ls

router = APIRouter()

@router.get("/fs/")
def read_fs(path: str):
    return fs_ls(path)
