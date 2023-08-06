from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpOrifice(PrimaryBase):
    __tablename__ = 'inp_orifice'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    node1 = Column(VARCHAR(250), autoincrement=False)
    node2 = Column(VARCHAR(250), autoincrement=False)
    type = Column(VARCHAR(25), autoincrement=False)
    offset = Column(VARCHAR(25), autoincrement=False)
    cd = Column(VARCHAR(25), autoincrement=False)
    flap = Column(VARCHAR(25), autoincrement=False)
    orate = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    mukey = Column(VARCHAR(191), autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    is_road = Column(INTEGER, autoincrement=False)
    location = Column(VARCHAR(191), autoincrement=False)
