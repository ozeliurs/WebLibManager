from datetime import datetime

from sqlmodel import Field, SQLModel


class File(SQLModel, table=True):
    path: str = Field(primary_key=True)
    size: int | None = None
    video_codec: str | None = None
    video_pix_fmt: str | None = None
    audio_codec: str | None = None
    subtitle_codec: str | None = None

class Job(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str
    created_at: str = datetime.now().isoformat()
    updated_at: str = Field(default_factory=datetime.now().isoformat)
