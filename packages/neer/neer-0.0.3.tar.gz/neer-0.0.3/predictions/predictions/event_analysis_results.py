from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class EventAnalysisResults(PrimaryBase):
    __tablename__ = 'event_analysis_results'
    __table_args__ = {'schema': 'predictions'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    site_id = Column(TEXT, nullable=False, autoincrement=False)
    dwf_simulation_id = Column(INTEGER, autoincrement=False)
    wwf_simulation_id = Column(INTEGER, autoincrement=False)
    event_id = Column(INTEGER, autoincrement=False)
    sewershed_id = Column(TEXT, autoincrement=False)
    groundwater_infiltration = Column(NUMERIC, autoincrement=False)
    gwi_per_idm = Column(NUMERIC, autoincrement=False)
    dry_weather_flow_ratio = Column(NUMERIC, autoincrement=False)
    ave_dry_weather_flow = Column(NUMERIC, autoincrement=False)
    total_i_i = Column(NUMERIC, autoincrement=False)
    r_value = Column(NUMERIC, autoincrement=False)
    i_i_per_idm = Column(NUMERIC, autoincrement=False)
    peak_flow = Column(NUMERIC, autoincrement=False)
    peaking_factor = Column(NUMERIC, autoincrement=False)
    peak_i_i = Column(NUMERIC, autoincrement=False)
    idm = Column(NUMERIC, autoincrement=False)
    peak_dwf = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
