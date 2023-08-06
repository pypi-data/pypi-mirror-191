from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkReportNodeLof(PrimaryBase):
    __tablename__ = 'spark_report_node_lof'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    name = Column(TEXT, primary_key=True, autoincrement=False)
    flow_area = Column(NUMERIC, autoincrement=False)
    ins_date = Column(DATE, autoincrement=False)
    pred_material = Column(BOOLEAN, autoincrement=False)
    pred_dim1 = Column(BOOLEAN, autoincrement=False)
    pred_dim2 = Column(BOOLEAN, autoincrement=False)
    pred_rimelev = Column(BOOLEAN, autoincrement=False)
    pred_invelev = Column(BOOLEAN, autoincrement=False)
    material = Column(TEXT, autoincrement=False)
    dim1 = Column(NUMERIC, autoincrement=False)
    dim2 = Column(NUMERIC, autoincrement=False)
    rim_ele = Column(NUMERIC, autoincrement=False)
    inv_ele = Column(NUMERIC, autoincrement=False)
    lof = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
