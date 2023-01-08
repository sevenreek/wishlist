from sqlmodel import SQLModel, Field
from datetime import datetime


class Timestamped(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
