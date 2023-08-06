from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpAquifer(PrimaryBase):
    __tablename__ = 'inp_aquifer'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    por = Column(VARCHAR(25), autoincrement=False)
    wp = Column(VARCHAR(25), autoincrement=False)
    fc = Column(VARCHAR(25), autoincrement=False)
    ksat = Column(VARCHAR(25), autoincrement=False)
    kslope = Column(VARCHAR(25), autoincrement=False)
    tslope = Column(VARCHAR(25), autoincrement=False)
    etu = Column(VARCHAR(25), autoincrement=False)
    ets = Column(VARCHAR(25), autoincrement=False)
    seep = Column(VARCHAR(25), autoincrement=False)
    ebot = Column(VARCHAR(25), autoincrement=False)
    egw = Column(VARCHAR(25), autoincrement=False)
    umc = Column(VARCHAR(25), autoincrement=False)
    etupat = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
