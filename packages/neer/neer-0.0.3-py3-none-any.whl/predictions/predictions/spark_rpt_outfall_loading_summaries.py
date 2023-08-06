from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptOutfallLoadingSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_outfall_loading_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    outfall_node = Column(TEXT, primary_key=True, autoincrement=False)
    flow_freq_percent = Column(NUMERIC, autoincrement=False)
    avg_flow_cfs = Column(NUMERIC, autoincrement=False)
    max_flow_cfs = Column(NUMERIC, autoincrement=False)
    total_volume = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
