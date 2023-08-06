from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpInfiltration(PrimaryBase):
    __tablename__ = 'inp_infiltration'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    subcatchment = Column(VARCHAR(250), autoincrement=False)
    maxrate = Column(VARCHAR(25), autoincrement=False)
    minrate = Column(VARCHAR(25), autoincrement=False)
    decay = Column(VARCHAR(25), autoincrement=False)
    drytime = Column(VARCHAR(25), autoincrement=False)
    maxinfil = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
