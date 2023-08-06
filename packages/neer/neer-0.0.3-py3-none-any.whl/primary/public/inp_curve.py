from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpCurve(PrimaryBase):
    __tablename__ = 'inp_curve'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    type = Column(VARCHAR(25), autoincrement=False)
    xvalue = Column('x-value', DOUBLE_PRECISION, autoincrement=False)
    yvalue = Column('y-value', DOUBLE_PRECISION, autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
