from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpSymbol(PrimaryBase):
    __tablename__ = 'inp_symbol'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    gage = Column(VARCHAR(250), autoincrement=False)
    xcoord = Column('x-coord', VARCHAR(25), autoincrement=False)
    ycoord = Column('y-coord', VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    lat = Column(VARCHAR(25), autoincrement=False)
    lng = Column(VARCHAR(25), autoincrement=False)
