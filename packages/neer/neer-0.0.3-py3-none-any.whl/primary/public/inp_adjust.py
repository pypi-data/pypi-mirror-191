from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpAdjust(PrimaryBase):
    __tablename__ = 'inp_adjust'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    parameter = Column(VARCHAR(50), nullable=False, autoincrement=False)
    subcatchment = Column(VARCHAR(50), autoincrement=False)
    m1 = Column(DOUBLE_PRECISION, autoincrement=False)
    m2 = Column(DOUBLE_PRECISION, autoincrement=False)
    m3 = Column(DOUBLE_PRECISION, autoincrement=False)
    m4 = Column(DOUBLE_PRECISION, autoincrement=False)
    m5 = Column(DOUBLE_PRECISION, autoincrement=False)
    m6 = Column(DOUBLE_PRECISION, autoincrement=False)
    m7 = Column(DOUBLE_PRECISION, autoincrement=False)
    m8 = Column(DOUBLE_PRECISION, autoincrement=False)
    m9 = Column(DOUBLE_PRECISION, autoincrement=False)
    m10 = Column(DOUBLE_PRECISION, autoincrement=False)
    m11 = Column(DOUBLE_PRECISION, autoincrement=False)
    m12 = Column(DOUBLE_PRECISION, autoincrement=False)
    flag = Column(INTEGER, autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
