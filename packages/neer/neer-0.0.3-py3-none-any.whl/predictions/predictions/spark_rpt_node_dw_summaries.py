from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptNodeDwSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_node_dw_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    node = Column(TEXT, primary_key=True, autoincrement=False)
    type = Column(TEXT, nullable=False, autoincrement=False)
    min_demand = Column(NUMERIC, autoincrement=False)
    max_demand = Column(NUMERIC, autoincrement=False)
    min_head = Column(NUMERIC, autoincrement=False)
    max_head = Column(NUMERIC, autoincrement=False)
    min_pressure = Column(NUMERIC, autoincrement=False)
    max_pressure = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    avg_demand = Column(NUMERIC, autoincrement=False)
    avg_head = Column(NUMERIC, autoincrement=False)
    avg_pressure = Column(NUMERIC, autoincrement=False)
