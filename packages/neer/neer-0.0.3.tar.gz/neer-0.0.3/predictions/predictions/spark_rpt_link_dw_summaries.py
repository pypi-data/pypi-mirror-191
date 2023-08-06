from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptLinkDwSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_link_dw_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    link = Column(TEXT, primary_key=True, autoincrement=False)
    type = Column(TEXT, nullable=False, autoincrement=False)
    min_flow = Column(NUMERIC, autoincrement=False)
    max_flow = Column(NUMERIC, autoincrement=False)
    min_velocity = Column(NUMERIC, autoincrement=False)
    max_velocity = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    avg_flow = Column(NUMERIC, autoincrement=False)
    avg_velocity = Column(NUMERIC, autoincrement=False)
