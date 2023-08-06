from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptPumpingSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_pumping_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    pump = Column(TEXT, primary_key=True, autoincrement=False)
    percent_utilized = Column(NUMERIC, autoincrement=False)
    number_of_start_ups = Column(INTEGER, autoincrement=False)
    min_flow_cfs = Column(NUMERIC, autoincrement=False)
    avg_flow_cfs = Column(NUMERIC, autoincrement=False)
    max_flow_cfs = Column(NUMERIC, autoincrement=False)
    total_volume = Column(NUMERIC, autoincrement=False)
    power_usage = Column(NUMERIC, autoincrement=False)
    percent_time_below_pump_curve = Column(NUMERIC, autoincrement=False)
    percent_time_above_pump_curve = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
