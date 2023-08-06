from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkRptStorageVolumeSummaries(PrimaryBase):
    __tablename__ = 'spark_rpt_storage_volume_summaries'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    storage_unit = Column(TEXT, primary_key=True, autoincrement=False)
    avg_volume = Column(NUMERIC, autoincrement=False)
    avg_percent_full = Column(INTEGER, autoincrement=False)
    evap_percent_loss = Column(NUMERIC, autoincrement=False)
    exfil_percent_loss = Column(NUMERIC, autoincrement=False)
    max_volume = Column(NUMERIC, autoincrement=False)
    total_volume = Column(NUMERIC, autoincrement=False)
    max_percent_full = Column(NUMERIC, autoincrement=False)
    day_of_max_volume = Column(INTEGER, autoincrement=False)
    hour_of_max_volume = Column(TIME, autoincrement=False)
    max_outflow_cfs = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
