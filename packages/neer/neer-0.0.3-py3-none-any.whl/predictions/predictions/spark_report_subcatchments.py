from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkReportSubcatchments(PrimaryBase):
    __tablename__ = 'spark_report_subcatchments'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    name = Column(TEXT, primary_key=True, autoincrement=False)
    datetime = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    date = Column(DATE, autoincrement=False)
    time = Column(TIME, autoincrement=False)
    is_forecasted = Column(BOOLEAN, primary_key=True, autoincrement=False)
    rainfall = Column(NUMERIC, autoincrement=False)
    snow = Column(NUMERIC, autoincrement=False)
    evap = Column(NUMERIC, autoincrement=False)
    infil = Column(NUMERIC, autoincrement=False)
    runoff = Column(NUMERIC, autoincrement=False)
    gw_flow = Column(NUMERIC, autoincrement=False)
    gw_elev = Column(NUMERIC, autoincrement=False)
    soil_moist = Column(NUMERIC, autoincrement=False)
    washoff = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
