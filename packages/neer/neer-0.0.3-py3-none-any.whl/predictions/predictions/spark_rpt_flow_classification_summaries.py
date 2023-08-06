from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptFlowClassificationSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_flow_classification_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    conduit = Column(TEXT, primary_key=True, autoincrement=False)
    adjusted_actual_length = Column(NUMERIC, autoincrement=False)
    fully_dry = Column(NUMERIC, autoincrement=False)
    upstream_dry = Column(NUMERIC, autoincrement=False)
    downstream_dry = Column(NUMERIC, autoincrement=False)
    sub_critical = Column(NUMERIC, autoincrement=False)
    super_critical = Column(NUMERIC, autoincrement=False)
    upstream_critical = Column(NUMERIC, autoincrement=False)
    downstream_critical = Column(NUMERIC, autoincrement=False)
    normal_flow_limited = Column(NUMERIC, autoincrement=False)
    inlet_control = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
