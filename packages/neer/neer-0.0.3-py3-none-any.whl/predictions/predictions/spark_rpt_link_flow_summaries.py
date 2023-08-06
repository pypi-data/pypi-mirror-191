from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptLinkFlowSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_link_flow_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    link = Column(TEXT, primary_key=True, autoincrement=False)
    type = Column(TEXT, autoincrement=False)
    max_flow_cfs = Column(NUMERIC, autoincrement=False)
    day_of_max_flow = Column(INTEGER, autoincrement=False)
    hour_of_max_flow = Column(TIME, autoincrement=False)
    max_velocity = Column(NUMERIC, autoincrement=False)
    max_full_flow = Column(NUMERIC, autoincrement=False)
    max_full_depth = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
