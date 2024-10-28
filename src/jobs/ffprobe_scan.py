import subprocess

from sqlmodel import Session, select

from ..models import File, Job
from ..database import engine

def ffprobe_scan(job_id: int):
    # List all files missing a video codec
    with Session(engine) as session:
        files = session.exec(select(File).where((File.video_codec == None) | (File.video_pix_fmt == None))).all()

        # Set job status to "scanning files metadata - video"
        job = session.get(Job, job_id)
        job.status = "scanning files metadata - video"
        session.add(job)
        session.commit()

        for file in files:
            ffprobe_video_scan_file(file, session)

        files = session.exec(select(File).where(File.audio_codec == None)).all()

        # Set job status to "scanning files metadata - video"
        job = session.get(Job, job_id)
        job.status = "scanning files metadata - audio"
        session.add(job)
        session.commit()

        for file in files:
            ffprobe_audio_scan_file(file, session)

        files = session.exec(select(File).where(File.subtitle_codec == None)).all()

        # Set job status to "scanning files metadata - subtitles"
        job = session.get(Job, job_id)
        job.status = "scanning files metadata - subtitles"
        session.add(job)
        session.commit()

        for file in files:
            ffprobe_subtitles_scan_file(file, session)


def ffprobe_video_scan_file(file: File, session: Session) -> None:
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,pix_fmt', '-of', 'default=noprint_wrappers=1:nokey=1', str(file.path)]
    ffprobe_output = subprocess.run(ffprobe_cmd, capture_output=True, text=True)

    if ffprobe_output.returncode != 0:
        return

    codec, pix_fmt = ffprobe_output.stdout.strip().split('\n')
    file.video_codec = codec
    file.video_pix_fmt = pix_fmt


    session.add(file)
    session.commit()

def ffprobe_audio_scan_file(file: File, session: Session) -> None:
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', str(file.path)]
    ffprobe_output = subprocess.run(ffprobe_cmd, capture_output=True, text=True)

    if ffprobe_output.returncode != 0:
        return

    codec = ffprobe_output.stdout.strip()
    file.audio_codec = codec

    session.add(file)
    session.commit()

def ffprobe_subtitles_scan_file(file: File, session: Session) -> None:
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 's:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', str(file.path)]
    ffprobe_output = subprocess.run(ffprobe_cmd, capture_output=True, text=True)

    if ffprobe_output.returncode != 0:
        return

    codec = ffprobe_output.stdout.strip()
    file.subtitle_codec = codec

    session.add(file)
    session.commit()
