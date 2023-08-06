from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkReportLinkCof(PrimaryBase):
    __tablename__ = 'spark_report_link_cof'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    name = Column(TEXT, primary_key=True, autoincrement=False)
    tmdl_imp = Column(NUMERIC, autoincrement=False)
    crit_imp = Column(NUMERIC, autoincrement=False)
    trans_imp = Column(NUMERIC, autoincrement=False)
    utility_imp = Column(NUMERIC, autoincrement=False)
    eco_imp = Column(NUMERIC, autoincrement=False)
    severity_imp = Column(NUMERIC, autoincrement=False)
    repl_cost = Column(NUMERIC, autoincrement=False)
    proxi_road = Column(NUMERIC, autoincrement=False)
    proxi_rail = Column(NUMERIC, autoincrement=False)
    proxi_gas = Column(NUMERIC, autoincrement=False)
    proxi_electric = Column(NUMERIC, autoincrement=False)
    cof = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
