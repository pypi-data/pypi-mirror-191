from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptNodeSurchargeSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_node_surcharge_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    node = Column(TEXT, primary_key=True, autoincrement=False)
    type = Column(TEXT, autoincrement=False)
    hours_surcharged = Column(NUMERIC, autoincrement=False)
    max_height_above_crown_feet = Column(NUMERIC, autoincrement=False)
    min_depth_below_rim_feet = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
