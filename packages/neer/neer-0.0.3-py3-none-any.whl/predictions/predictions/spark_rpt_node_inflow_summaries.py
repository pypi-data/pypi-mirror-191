from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptNodeInflowSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_node_inflow_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    node = Column(TEXT, primary_key=True, autoincrement=False)
    type = Column(TEXT, autoincrement=False)
    max_lateral_inflow_cfs = Column(NUMERIC, autoincrement=False)
    max_total_inflow_cfs = Column(NUMERIC, autoincrement=False)
    day_of_max_inflow = Column(INTEGER, autoincrement=False)
    hour_of_max_inflow = Column(TIME, autoincrement=False)
    lateral_inflow_volume = Column(NUMERIC, autoincrement=False)
    total_inflow_volume = Column(NUMERIC, autoincrement=False)
    flow_balance_error_percent = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
