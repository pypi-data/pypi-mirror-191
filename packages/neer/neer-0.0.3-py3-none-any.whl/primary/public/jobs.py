from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, SMALLINT
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Jobs(PrimaryBase):
    __tablename__ = 'jobs'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    queue = Column(VARCHAR(191), nullable=False, autoincrement=False)
    payload = Column(TEXT, nullable=False, autoincrement=False)
    attempts = Column(SMALLINT, nullable=False, autoincrement=False)
    reserved_at = Column(INTEGER, autoincrement=False)
    available_at = Column(INTEGER, nullable=False, autoincrement=False)
    created_at = Column(INTEGER, nullable=False, autoincrement=False)
