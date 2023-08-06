from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class FailedJobs(PrimaryBase):
    __tablename__ = 'failed_jobs'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    connection = Column(TEXT, nullable=False, autoincrement=False)
    queue = Column(TEXT, nullable=False, autoincrement=False)
    payload = Column(TEXT, nullable=False, autoincrement=False)
    exception = Column(TEXT, nullable=False, autoincrement=False)
    failed_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
