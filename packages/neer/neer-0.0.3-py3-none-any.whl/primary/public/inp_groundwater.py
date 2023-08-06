from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpGroundwater(PrimaryBase):
    __tablename__ = 'inp_groundwater'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    subcatchment = Column(VARCHAR(250), autoincrement=False)
    aquifer = Column(VARCHAR(250), autoincrement=False)
    node = Column(VARCHAR(250), autoincrement=False)
    esurf = Column(VARCHAR(25), autoincrement=False)
    a1 = Column(VARCHAR(25), autoincrement=False)
    b1 = Column(VARCHAR(25), autoincrement=False)
    a2 = Column(VARCHAR(25), autoincrement=False)
    b2 = Column(VARCHAR(25), autoincrement=False)
    a3 = Column(VARCHAR(25), autoincrement=False)
    dsw = Column(VARCHAR(25), autoincrement=False)
    egwt = Column(VARCHAR(25), autoincrement=False)
    ebot = Column(VARCHAR(25), autoincrement=False)
    wgr = Column(VARCHAR(25), autoincrement=False)
    umc = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
