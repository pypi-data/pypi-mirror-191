from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpSnowpackValues(PrimaryBase):
    __tablename__ = 'inp_snowpack_values'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    inp_snowpack_id = Column(BIGINT, nullable=False, autoincrement=False)
    surface = Column(VARCHAR(30), nullable=False, autoincrement=False)
    parameter1 = Column(DOUBLE_PRECISION, autoincrement=False)
    parameter2 = Column(DOUBLE_PRECISION, autoincrement=False)
    parameter3 = Column(DOUBLE_PRECISION, autoincrement=False)
    parameter4 = Column(DOUBLE_PRECISION, autoincrement=False)
    parameter5 = Column(DOUBLE_PRECISION, autoincrement=False)
    parameter6 = Column(DOUBLE_PRECISION, autoincrement=False)
    parameter7 = Column(DOUBLE_PRECISION, autoincrement=False)
    subcatchment = Column(VARCHAR(50), autoincrement=False)
