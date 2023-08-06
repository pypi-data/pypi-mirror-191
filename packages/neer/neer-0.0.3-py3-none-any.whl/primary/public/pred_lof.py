from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class PredLof(PrimaryBase):
    __tablename__ = 'pred_lof'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    link_id = Column(INTEGER, nullable=False, autoincrement=False)
    pred_lof = Column(VARCHAR(25), nullable=False, autoincrement=False)
    yval_lof = Column(VARCHAR(25), nullable=False, autoincrement=False)
    created_on = Column(TIMESTAMP, nullable=False, autoincrement=False)
