from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpCurveDw(PrimaryBase):
    __tablename__ = 'inp_curve_dw'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), nullable=False, autoincrement=False)
    type = Column(VARCHAR(25), nullable=False, autoincrement=False)
    xvalue = Column('x-value', DOUBLE_PRECISION, autoincrement=False)
    yvalue = Column('y-value', DOUBLE_PRECISION, autoincrement=False)
    description = Column(TEXT, autoincrement=False)
