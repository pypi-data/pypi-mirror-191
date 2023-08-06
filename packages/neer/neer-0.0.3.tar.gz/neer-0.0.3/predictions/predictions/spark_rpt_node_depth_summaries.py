from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptNodeDepthSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_node_depth_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    node = Column(TEXT, primary_key=True, autoincrement=False)
    type = Column(TEXT, autoincrement=False)
    avg_depth_feet = Column(NUMERIC, autoincrement=False)
    max_depth_feet = Column(NUMERIC, autoincrement=False)
    max_hgl_feet = Column(NUMERIC, autoincrement=False)
    day_of_maximum_depth = Column(INTEGER, autoincrement=False)
    hour_of_maximum_depth = Column(TIME, autoincrement=False)
    max_reported_depth_feet = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
