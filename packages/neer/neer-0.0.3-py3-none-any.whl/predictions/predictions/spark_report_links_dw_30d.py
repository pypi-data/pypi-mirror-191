from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SparkReportLinksDw30d(PrimaryBase):
    __tablename__ = 'spark_report_links_dw_30d'
    __table_args__ = {'schema': 'predictions'}
    
    bucket = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    name = Column(TEXT, primary_key=True, autoincrement=False)
    layer = Column(TEXT, autoincrement=False)
    state = Column(TEXT, autoincrement=False)
    avg_flow = Column(NUMERIC, autoincrement=False)
    avg_velocity = Column(NUMERIC, autoincrement=False)
    avg_headloss = Column(NUMERIC, autoincrement=False)
    avg_setting = Column(NUMERIC, autoincrement=False)
    avg_reaction = Column(NUMERIC, autoincrement=False)
    avg_f_factor = Column(NUMERIC, autoincrement=False)
    min_flow = Column(NUMERIC, autoincrement=False)
    min_velocity = Column(NUMERIC, autoincrement=False)
    min_headloss = Column(NUMERIC, autoincrement=False)
    min_setting = Column(NUMERIC, autoincrement=False)
    min_reaction = Column(NUMERIC, autoincrement=False)
    min_f_factor = Column(NUMERIC, autoincrement=False)
    max_flow = Column(NUMERIC, autoincrement=False)
    max_velocity = Column(NUMERIC, autoincrement=False)
    max_headloss = Column(NUMERIC, autoincrement=False)
    max_setting = Column(NUMERIC, autoincrement=False)
    max_reaction = Column(NUMERIC, autoincrement=False)
    max_f_factor = Column(NUMERIC, autoincrement=False)
    is_forecasted = Column(BOOLEAN, primary_key=True, autoincrement=False)
