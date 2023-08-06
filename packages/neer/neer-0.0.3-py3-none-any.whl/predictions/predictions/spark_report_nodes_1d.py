from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, ARRAY
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkReportNodes1d(PrimaryBase):
    __tablename__ = 'spark_report_nodes_1d'
    __table_args__ = {'schema': 'predictions'}
    
    bucket = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    name = Column(TEXT, primary_key=True, autoincrement=False)
    is_forecasted = Column(BOOLEAN, primary_key=True, autoincrement=False)
    avg_depth = Column(NUMERIC, autoincrement=False)
    avg_head = Column(NUMERIC, autoincrement=False)
    avg_volume = Column(NUMERIC, autoincrement=False)
    avg_lateral = Column(NUMERIC, autoincrement=False)
    avg_inflow = Column(NUMERIC, autoincrement=False)
    avg_flooding = Column(NUMERIC, autoincrement=False)
    min_depth = Column(NUMERIC, autoincrement=False)
    min_head = Column(NUMERIC, autoincrement=False)
    min_volume = Column(NUMERIC, autoincrement=False)
    min_lateral = Column(NUMERIC, autoincrement=False)
    min_inflow = Column(NUMERIC, autoincrement=False)
    min_flooding = Column(NUMERIC, autoincrement=False)
    max_depth = Column(NUMERIC, autoincrement=False)
    max_head = Column(NUMERIC, autoincrement=False)
    max_volume = Column(NUMERIC, autoincrement=False)
    max_lateral = Column(NUMERIC, autoincrement=False)
    max_inflow = Column(NUMERIC, autoincrement=False)
    max_flooding = Column(NUMERIC, autoincrement=False)
    avg_qualities = Column(ARRAY(NUMERIC), autoincrement=False)
    min_qualities = Column(ARRAY(NUMERIC), autoincrement=False)
    max_qualities = Column(ARRAY(NUMERIC), autoincrement=False)
