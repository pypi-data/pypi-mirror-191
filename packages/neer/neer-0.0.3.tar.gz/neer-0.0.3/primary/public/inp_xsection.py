from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpXsection(PrimaryBase):
    __tablename__ = 'inp_xsection'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    link = Column(VARCHAR(250), autoincrement=False)
    type = Column(VARCHAR(25), autoincrement=False)
    geom1 = Column(VARCHAR(25), autoincrement=False)
    geom2 = Column(VARCHAR(25), autoincrement=False)
    geom3 = Column(VARCHAR(25), autoincrement=False)
    geom4 = Column(VARCHAR(25), autoincrement=False)
    barrels = Column(VARCHAR(25), autoincrement=False)
    culvert = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
