from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import expression

Base = declarative_base()


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class BaseModel(Base):
    """
    Base model with datetimes for when records are created and updated
    """

    __abstract__ = True

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    created_at = Column(DateTime(), nullable=False, server_default=utcnow())
    updated_at = Column(
        DateTime(), nullable=False, server_default=utcnow(), onupdate=utcnow()
    )


# Set the fields to be the last fields created
BaseModel.created_at._creation_order = 9998
BaseModel.updated_at._creation_order = 9999
