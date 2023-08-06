from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpEvaporation(PrimaryBase):
    __tablename__ = 'inp_evaporation'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    type = Column(VARCHAR(25), autoincrement=False)
    field_value = Column(VARCHAR(50), autoincrement=False)
    p1 = Column(DOUBLE_PRECISION, autoincrement=False)
    p2 = Column(DOUBLE_PRECISION, autoincrement=False)
    p3 = Column(DOUBLE_PRECISION, autoincrement=False)
    p4 = Column(DOUBLE_PRECISION, autoincrement=False)
    p5 = Column(DOUBLE_PRECISION, autoincrement=False)
    p6 = Column(DOUBLE_PRECISION, autoincrement=False)
    p7 = Column(DOUBLE_PRECISION, autoincrement=False)
    p8 = Column(DOUBLE_PRECISION, autoincrement=False)
    p9 = Column(DOUBLE_PRECISION, autoincrement=False)
    p10 = Column(DOUBLE_PRECISION, autoincrement=False)
    p11 = Column(DOUBLE_PRECISION, autoincrement=False)
    p12 = Column(DOUBLE_PRECISION, autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
