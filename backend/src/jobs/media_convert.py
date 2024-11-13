import os
import subprocess
import logging
from pathlib import Path
from typing import Optional
from sqlmodel import Session
from ..models import Job, File
from ..database import engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConversionError(Exception):
    """Custom exception for conversion-related errors"""
    pass

class MediaConverter:
    def __init__(self, session: Session, job_id: int, file_path: str):
        self.session = session
        self.job_id = job_id
        self.job = self._get_job()
        self.file_path = Path(file_path)
        self.output_dir = self.file_path.parent
        self.output_path = self.output_dir / f"{self.file_path.stem}_converted{self.file_path.suffix}"

    def _get_job(self) -> Optional[Job]:
        job = self.session.get(Job, self.job_id)
        if not job:
            raise ConversionError(f"Job with id {self.job_id} not found")
        return job

    def _update_job_status(self, status: str) -> None:
        if self.job:
            self.job.status = status
            self.session.add(self.job)
            self.session.commit()
            logger.info(f"Job {self.job_id} status updated to: {status}")

    def _ensure_output_directory(self) -> None:
        """Ensure output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)

    def _build_ffmpeg_command(self) -> list:
        """Build FFmpeg command for conversion"""
        return [
            'ffmpeg',
            '-i', str(self.file_path),
            # Video settings
            '-c:v', 'libx264',     # H.264 video codec
            '-preset', 'medium',    # Encoding preset (balance between speed and quality)
            '-crf', '23',          # Constant Rate Factor (quality setting, lower = better)
            # Audio settings
            '-c:a', 'aac',         # AAC audio codec
            '-b:a', '192k',        # Audio bitrate
            # Subtitle settings
            '-c:s', 'srt',         # SRT subtitle format
            # General settings
            '-movflags', '+faststart',  # Enable fast start for web playback
            '-y',                   # Overwrite output file if exists
            str(self.output_path)
        ]

    def convert(self) -> None:
        """Execute the media conversion"""
        try:
            self._ensure_output_directory()
            self._update_job_status("converting")

            cmd = self._build_ffmpeg_command()

            # Run FFmpeg command
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Monitor the conversion process
            while True:
                output = process.stderr.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    logger.debug(output.strip())

            if process.returncode != 0:
                raise ConversionError("FFmpeg conversion failed")

            # Update job status to completed
            self._update_job_status("completed")
            logger.info(f"Successfully converted {self.file_path} to {self.output_path}")

        except Exception as e:
            error_msg = f"Conversion failed: {str(e)}"
            logger.error(error_msg)
            self._update_job_status(f"failed - {error_msg}")
            raise ConversionError(error_msg)

def media_convert(file_path: str, job_id: int) -> None:
    """Main entry point for media conversion"""
    try:
        with Session(engine) as session:
            converter = MediaConverter(session, job_id, file_path)
            converter.convert()
    except Exception as e:
        logger.error(f"Conversion error: {e}")
