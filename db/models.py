from sqlalchemy import Column, BigInteger, func, DateTime, VARCHAR
from sqlalchemy.ext.mutable import MutableDict

from sqlalchemy.dialects.postgresql import JSONB

from config import Config
from db.base.base import Base


class User(Base):
    config = Config()
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    fullname = Column(VARCHAR(128), nullable=False)
    username = Column(VARCHAR(32), nullable=True)
    creation_date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    inventory = Column(MutableDict.as_mutable(JSONB()), default={})
    history = Column(MutableDict.as_mutable(JSONB()), default={})
