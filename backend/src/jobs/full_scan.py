import logging
from pathlib import Path
from typing import Optional
from sqlmodel import Session
from contextlib import contextmanager

from .fs_scan import fs_scan
from .ffprobe_scan import ffprobe_scan
from ..models import Job
from ..database import engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ScanError(Exception):
    """Custom exception for scan-related errors"""
    pass

class JobManager:
    def __init__(self, job_id: int):
        self.job_id = job_id

    @contextmanager
    def get_session(self):
        """Context manager for database sessions"""
        session = Session(engine)
        try:
            yield session
        finally:
            session.close()

    def get_job(self, session: Session) -> Optional[Job]:
        """Retrieve job from database"""
        job = session.get(Job, self.job_id)
        if not job:
            raise ScanError(f"Job {self.job_id} not found")
        return job

    def update_status(self, status: str) -> None:
        """Update job status in database"""
        try:
            with self.get_session() as session:
                job = self.get_job(session)
                job.status = status
                session.add(job)
                session.commit()
                logger.info(f"Job {self.job_id} status updated to: {status}")
        except Exception as e:
            logger.error(f"Failed to update job status: {e}")
            raise ScanError(f"Failed to update job status: {e}")

class Scanner:
    def __init__(self, path: str, job_manager: JobManager):
        self.path = Path(path)
        self.job_manager = job_manager

    def validate_path(self) -> None:
        """Validate the scan path"""
        if not self.path.exists():
            raise ScanError(f"Path does not exist: {self.path}")
        if not self.path.is_dir():
            raise ScanError(f"Path is not a directory: {self.path}")

    def run_filesystem_scan(self) -> None:
        """Run filesystem scan"""
        try:
            self.job_manager.update_status("scanning files")
            fs_scan(str(self.path))
            logger.info("Filesystem scan completed successfully")
        except Exception as e:
            logger.error(f"Filesystem scan failed: {e}")
            raise ScanError(f"Filesystem scan failed: {e}")

    def run_ffprobe_scan(self) -> None:
        """Run ffprobe scan"""
        try:
            self.job_manager.update_status("scanning files metadata")
            ffprobe_scan(self.job_manager.job_id)
            logger.info("FFprobe scan completed successfully")
        except Exception as e:
            logger.error(f"FFprobe scan failed: {e}")
            raise ScanError(f"FFprobe scan failed: {e}")

    def run_full_scan(self) -> None:
        """Run complete scan process"""
        try:
            self.validate_path()
            self.run_filesystem_scan()
            self.run_ffprobe_scan()
            self.job_manager.update_status("completed")
            logger.info("Full scan completed successfully")
        except ScanError as e:
            self.job_manager.update_status(f"failed - {str(e)}")
            logger.error(f"Scan failed: {e}")
            raise
        except Exception as e:
            self.job_manager.update_status(f"failed - unexpected error")
            logger.error(f"Unexpected error during scan: {e}")
            raise ScanError(f"Unexpected error during scan: {e}")

def full_scan(path: str, job_id: int) -> None:
    """Main entry point for full scan operation"""
    try:
        job_manager = JobManager(job_id)
        scanner = Scanner(path, job_manager)
        scanner.run_full_scan()
    except ScanError as e:
        logger.error(f"Scan error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        try:
            job_manager.update_status(f"failed - unexpected error")
        except Exception as update_error:
            logger.error(f"Failed to update error status: {update_error}")
