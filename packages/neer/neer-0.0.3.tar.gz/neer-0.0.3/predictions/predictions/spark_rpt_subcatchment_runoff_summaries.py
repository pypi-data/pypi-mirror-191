from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptSubcatchmentRunoffSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_subcatchment_runoff_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    subcatchment = Column(TEXT, primary_key=True, autoincrement=False)
    total_precip_in = Column(NUMERIC, autoincrement=False)
    total_runon_in = Column(NUMERIC, autoincrement=False)
    total_evap_in = Column(NUMERIC, autoincrement=False)
    total_infil_in = Column(NUMERIC, autoincrement=False)
    imperv_runoff_in = Column(NUMERIC, autoincrement=False)
    perv_runoff_in = Column(NUMERIC, autoincrement=False)
    total_runoff_in = Column(NUMERIC, autoincrement=False)
    total_runoff_gallons = Column(NUMERIC, autoincrement=False)
    peak_runoff_cfs = Column(NUMERIC, autoincrement=False)
    runoff_coeff = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
