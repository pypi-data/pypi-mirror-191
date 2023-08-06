from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpDwf(PrimaryBase):
    __tablename__ = 'inp_dwf'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    node = Column(VARCHAR(250), autoincrement=False)
    parameter = Column(VARCHAR(25), autoincrement=False)
    average_value = Column(VARCHAR(25), autoincrement=False)
    tp1 = Column(VARCHAR(255), autoincrement=False)
    tp2 = Column(VARCHAR(255), autoincrement=False)
    tp3 = Column(VARCHAR(255), autoincrement=False)
    tp4 = Column(VARCHAR(255), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
