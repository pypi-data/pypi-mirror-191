from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkReportNodesDw30d(PrimaryBase):
    __tablename__ = 'spark_report_nodes_dw_30d'
    __table_args__ = {'schema': 'predictions'}
    
    bucket = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    name = Column(TEXT, primary_key=True, autoincrement=False)
    layer = Column(TEXT, autoincrement=False)
    avg_demand = Column(NUMERIC, autoincrement=False)
    avg_head = Column(NUMERIC, autoincrement=False)
    avg_pressure = Column(NUMERIC, autoincrement=False)
    avg_quality_parameter = Column(NUMERIC, autoincrement=False)
    min_demand = Column(NUMERIC, autoincrement=False)
    min_head = Column(NUMERIC, autoincrement=False)
    min_pressure = Column(NUMERIC, autoincrement=False)
    min_quality_parameter = Column(NUMERIC, autoincrement=False)
    max_demand = Column(NUMERIC, autoincrement=False)
    max_head = Column(NUMERIC, autoincrement=False)
    max_pressure = Column(NUMERIC, autoincrement=False)
    max_quality_parameter = Column(NUMERIC, autoincrement=False)
    is_forecasted = Column(BOOLEAN, primary_key=True, autoincrement=False)
