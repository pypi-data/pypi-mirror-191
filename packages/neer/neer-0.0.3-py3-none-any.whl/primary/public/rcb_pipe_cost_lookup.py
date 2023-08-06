from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class RcbPipeCostLookup(PrimaryBase):
    __tablename__ = 'rcb_pipe_cost_lookup'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    object_id = Column(INTEGER, nullable=False, autoincrement=False)
    min_flow_area = Column(INTEGER, nullable=False, autoincrement=False)
    max_flow_area = Column(INTEGER, nullable=False, autoincrement=False)
    lnft_unit_cost_under_pavement = Column(INTEGER, nullable=False, autoincrement=False)
    lnft_unit_cost_not_under_pavement = Column(INTEGER, nullable=False, autoincrement=False)
    lnft_cost_near_rail = Column(INTEGER, nullable=False, autoincrement=False)
