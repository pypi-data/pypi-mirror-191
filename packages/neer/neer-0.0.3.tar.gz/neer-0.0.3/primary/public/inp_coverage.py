from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpCoverage(PrimaryBase):
    __tablename__ = 'inp_coverage'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    subcatchment = Column(VARCHAR(250), autoincrement=False)
    landuse = Column(VARCHAR(25), autoincrement=False)
    percent = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
