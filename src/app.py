from fastapi import FastAPI

from .database import create_db_and_tables
from .routers import scan, fs, files

app = FastAPI()

app.include_router(scan.router, prefix="/api")
app.include_router(fs.router, prefix="/api")
app.include_router(files.router, prefix="/api")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
