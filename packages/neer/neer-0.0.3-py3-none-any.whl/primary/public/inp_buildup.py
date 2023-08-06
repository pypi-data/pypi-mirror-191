from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpBuildup(PrimaryBase):
    __tablename__ = 'inp_buildup'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    landuse = Column(VARCHAR(250), autoincrement=False)
    pollutant = Column(VARCHAR(250), autoincrement=False)
    function = Column(VARCHAR(25), autoincrement=False)
    coeff1 = Column(VARCHAR(25), autoincrement=False)
    coeff2 = Column(VARCHAR(25), autoincrement=False)
    coeff3 = Column(VARCHAR(25), autoincrement=False)
    normalizer = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
