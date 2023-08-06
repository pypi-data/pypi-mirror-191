from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkReportLinkLof(PrimaryBase):
    __tablename__ = 'spark_report_link_lof'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    name = Column(TEXT, primary_key=True, autoincrement=False)
    flow_area = Column(NUMERIC, autoincrement=False)
    pred_material = Column(BOOLEAN, autoincrement=False)
    pred_dsinvelev = Column(BOOLEAN, autoincrement=False)
    pred_usinvelev = Column(BOOLEAN, autoincrement=False)
    material = Column(TEXT, autoincrement=False)
    ds_inv_elev = Column(NUMERIC, autoincrement=False)
    us_inv_elev = Column(NUMERIC, autoincrement=False)
    lof = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
