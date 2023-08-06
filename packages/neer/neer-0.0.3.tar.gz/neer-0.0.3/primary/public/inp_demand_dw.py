from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpDemandDw(PrimaryBase):
    __tablename__ = 'inp_demand_dw'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    junction = Column(VARCHAR(191), nullable=False, autoincrement=False)
    demand = Column(VARCHAR(191), nullable=False, autoincrement=False)
    pattern = Column(VARCHAR(191), autoincrement=False)
    category = Column(VARCHAR(191), autoincrement=False)
