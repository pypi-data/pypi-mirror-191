from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptConduitSurchargeSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_conduit_surcharge_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    conduit = Column(TEXT, primary_key=True, autoincrement=False)
    hours_both_ends_full = Column(NUMERIC, autoincrement=False)
    hours_upstream_full = Column(NUMERIC, autoincrement=False)
    hours_downstream_full = Column(NUMERIC, autoincrement=False)
    hours_above_normal_flow = Column(NUMERIC, autoincrement=False)
    hours_capacity_limited = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
