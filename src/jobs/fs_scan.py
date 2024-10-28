import os

from sqlmodel import Session, select

from ..models import File
from ..database import engine

def fs_ls(path: str):
    items = os.listdir(path)
    dirs = []
    files = []

    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            dirs.append(item)
        else:
            files.append(item)

    return dirs, files

def fs_scan(base_path: str):
    visited_files = set()

    with Session(engine) as session:
        # Walk through directory tree
        for root, _, files in os.walk(base_path):
            for filename in files:
                full_path = os.path.join(root, filename)

                # Skip if already processed
                if full_path in visited_files:
                    continue

                visited_files.add(full_path)

                # Get file size
                try:
                    size = os.path.getsize(full_path)
                except OSError:
                    continue

                # Check if file record already exists
                existing_record = session.exec(
                    select(File).where(File.path == full_path)
                ).first()

                if existing_record is None:
                    # Create and save file record only if it doesn't exist
                    file_record = File(path=full_path, size=size)
                    session.add(file_record)

        session.commit()
