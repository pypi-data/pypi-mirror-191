from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpEvent(PrimaryBase):
    __tablename__ = 'inp_event'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    start_date = Column(TIMESTAMP, nullable=False, autoincrement=False)
    end_date = Column(TIMESTAMP, nullable=False, autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
