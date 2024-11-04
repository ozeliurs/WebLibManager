import subprocess
from enum import Enum
from typing import Sequence
from typing import Optional
from sqlmodel import Session, select
from ..models import File, Job
from ..database import engine

class ScanType(Enum):
    VIDEO = ("v:0", "scanning files metadata - video")
    AUDIO = ("a:0", "scanning files metadata - audio")
    SUBTITLES = ("s:0", "scanning files metadata - subtitles")

class FFProbeScan:
    def __init__(self, session: Session, job_id: int):
        self.session = session
        self.job_id = job_id
        self.job = self._get_job()

    def _get_job(self) -> Optional[Job]:
        job = self.session.get(Job, self.job_id)
        if not job:
            raise ValueError(f"Job with id {self.job_id} not found")
        return job

    def _update_job_status(self, status: str) -> None:
        if self.job:
            self.job.status = status
            self.session.add(self.job)
            self.session.commit()

    def _get_files_to_scan(self, scan_type: ScanType) -> Sequence[File]:
        if scan_type == ScanType.VIDEO:
            return self.session.exec(
                select(File).where((File.video_codec == None) | (File.video_pix_fmt == None))
            ).all()
        elif scan_type == ScanType.AUDIO:
            return self.session.exec(
                select(File).where(File.audio_codec == None)
            ).all()
        else:  # SUBTITLES
            return self.session.exec(
                select(File).where(File.subtitle_codec == None)
            ).all()

    def _run_ffprobe(self, file_path: str, stream_selector: str, entries: str) -> Optional[str]:
        cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', stream_selector,
            '-show_entries', f'stream={entries}',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(file_path)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def _scan_video(self, file: File) -> None:
        output = self._run_ffprobe(file.path, "v:0", "codec_name,pix_fmt")
        if output and '\n' in output:
            codec, pix_fmt = output.split('\n')
            file.video_codec = codec
            file.video_pix_fmt = pix_fmt
            self._save_file(file)

    def _scan_audio(self, file: File) -> None:
        output = self._run_ffprobe(file.path, "a:0", "codec_name")
        if output:
            file.audio_codec = output
            self._save_file(file)

    def _scan_subtitles(self, file: File) -> None:
        output = self._run_ffprobe(file.path, "s:0", "codec_name")
        if output:
            file.subtitle_codec = output
            self._save_file(file)

    def _save_file(self, file: File) -> None:
        self.session.add(file)
        self.session.commit()

    def scan_files(self) -> None:
        for scan_type in ScanType:
            self._update_job_status(scan_type.value[1])
            files = self._get_files_to_scan(scan_type)

            for file in files:
                if scan_type == ScanType.VIDEO:
                    self._scan_video(file)
                elif scan_type == ScanType.AUDIO:
                    self._scan_audio(file)
                else:  # SUBTITLES
                    self._scan_subtitles(file)

def ffprobe_scan(job_id: int) -> None:
    with Session(engine) as session:
        scanner = FFProbeScan(session, job_id)
        scanner.scan_files()
