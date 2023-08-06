from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, ARRAY
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkReportLinks1h(PrimaryBase):
    __tablename__ = 'spark_report_links_1h'
    __table_args__ = {'schema': 'predictions'}
    
    bucket = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    name = Column(TEXT, primary_key=True, autoincrement=False)
    is_forecasted = Column(BOOLEAN, primary_key=True, autoincrement=False)
    avg_flow = Column(NUMERIC, autoincrement=False)
    avg_depth = Column(NUMERIC, autoincrement=False)
    avg_velocity = Column(NUMERIC, autoincrement=False)
    avg_volume = Column(NUMERIC, autoincrement=False)
    avg_capacity = Column(NUMERIC, autoincrement=False)
    min_flow = Column(NUMERIC, autoincrement=False)
    min_depth = Column(NUMERIC, autoincrement=False)
    min_velocity = Column(NUMERIC, autoincrement=False)
    min_volume = Column(NUMERIC, autoincrement=False)
    min_capacity = Column(NUMERIC, autoincrement=False)
    max_flow = Column(NUMERIC, autoincrement=False)
    max_depth = Column(NUMERIC, autoincrement=False)
    max_velocity = Column(NUMERIC, autoincrement=False)
    max_volume = Column(NUMERIC, autoincrement=False)
    max_capacity = Column(NUMERIC, autoincrement=False)
    avg_qualities = Column(ARRAY(NUMERIC), autoincrement=False)
    min_qualities = Column(ARRAY(NUMERIC), autoincrement=False)
    max_qualities = Column(ARRAY(NUMERIC), autoincrement=False)
