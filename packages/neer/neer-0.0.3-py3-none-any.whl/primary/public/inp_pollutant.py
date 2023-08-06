from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpPollutant(PrimaryBase):
    __tablename__ = 'inp_pollutant'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    mass_units = Column(VARCHAR(25), autoincrement=False)
    crain = Column(VARCHAR(25), autoincrement=False)
    cgw = Column(VARCHAR(25), autoincrement=False)
    crdii = Column(VARCHAR(25), autoincrement=False)
    kdecay = Column(VARCHAR(25), autoincrement=False)
    snow_only = Column(VARCHAR(25), autoincrement=False)
    co_pollutant = Column(VARCHAR(25), autoincrement=False)
    cdwf = Column(VARCHAR(10), autoincrement=False)
    cinit = Column(VARCHAR(10), autoincrement=False)
    co_frac = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
