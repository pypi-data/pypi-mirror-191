from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class ApiJobs(PrimaryBase):
    __tablename__ = 'api_jobs'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    env = Column(VARCHAR(191), autoincrement=False)
    action = Column(VARCHAR(191), autoincrement=False)
    payload = Column(TEXT, autoincrement=False)
    attempts = Column(INTEGER, nullable=False, autoincrement=False)
    error = Column(TEXT, autoincrement=False)
    response = Column(TEXT, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
