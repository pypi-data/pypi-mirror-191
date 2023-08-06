from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptNodeFloodingSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_node_flooding_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    node = Column(TEXT, primary_key=True, autoincrement=False)
    hours_flooded = Column(NUMERIC, autoincrement=False)
    max_rate_cfs = Column(NUMERIC, autoincrement=False)
    day_of_max_flooding = Column(INTEGER, autoincrement=False)
    hour_of_max_flooding = Column(TIME, autoincrement=False)
    total_flood_volume = Column(NUMERIC, autoincrement=False)
    max_ponded_depth_feet = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
