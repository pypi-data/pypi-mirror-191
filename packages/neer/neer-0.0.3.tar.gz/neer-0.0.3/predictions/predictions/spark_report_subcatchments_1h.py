from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkReportSubcatchments1h(PrimaryBase):
    __tablename__ = 'spark_report_subcatchments_1h'
    __table_args__ = {'schema': 'predictions'}
    
    bucket = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    name = Column(TEXT, primary_key=True, autoincrement=False)
    is_forecasted = Column(BOOLEAN, primary_key=True, autoincrement=False)
    avg_rainfall = Column(NUMERIC, autoincrement=False)
    avg_snow = Column(NUMERIC, autoincrement=False)
    avg_evap = Column(NUMERIC, autoincrement=False)
    avg_infil = Column(NUMERIC, autoincrement=False)
    avg_runoff = Column(NUMERIC, autoincrement=False)
    avg_gw_flow = Column(NUMERIC, autoincrement=False)
    avg_gw_elev = Column(NUMERIC, autoincrement=False)
    avg_soil_moist = Column(NUMERIC, autoincrement=False)
    avg_washoff = Column(NUMERIC, autoincrement=False)
    min_rainfall = Column(NUMERIC, autoincrement=False)
    min_snow = Column(NUMERIC, autoincrement=False)
    min_evap = Column(NUMERIC, autoincrement=False)
    min_infil = Column(NUMERIC, autoincrement=False)
    min_runoff = Column(NUMERIC, autoincrement=False)
    min_gw_flow = Column(NUMERIC, autoincrement=False)
    min_gw_elev = Column(NUMERIC, autoincrement=False)
    min_soil_moist = Column(NUMERIC, autoincrement=False)
    min_washoff = Column(NUMERIC, autoincrement=False)
    max_rainfall = Column(NUMERIC, autoincrement=False)
    max_snow = Column(NUMERIC, autoincrement=False)
    max_evap = Column(NUMERIC, autoincrement=False)
    max_infil = Column(NUMERIC, autoincrement=False)
    max_runoff = Column(NUMERIC, autoincrement=False)
    max_gw_flow = Column(NUMERIC, autoincrement=False)
    max_gw_elev = Column(NUMERIC, autoincrement=False)
    max_soil_moist = Column(NUMERIC, autoincrement=False)
    max_washoff = Column(NUMERIC, autoincrement=False)
