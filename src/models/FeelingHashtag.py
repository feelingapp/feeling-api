import uuid

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models import Base

FeelingHashtag = Table(
    "feeling_hashtags",
    Base.metadata,
    Column("feeling_id", UUID(as_uuid=True), ForeignKey("feelings.id")),
    Column("hashtag_id", UUID(as_uuid=True), ForeignKey("hashtags.id")),
)
