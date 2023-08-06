from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class LeakDetectionProgram(PrimaryBase):
    __tablename__ = 'leak_detection_program'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    service_area = Column(VARCHAR(191), nullable=False, autoincrement=False)
    leaks = Column(INTEGER, nullable=False, autoincrement=False)
    days = Column(INTEGER, nullable=False, autoincrement=False)
    miles_walked = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    leaks_per_days = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    leaks_per_mile = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
