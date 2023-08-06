from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class LikelyLeakLocations(PrimaryBase):
    __tablename__ = 'likely_leak_locations'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    leak_id = Column(INTEGER, nullable=False, autoincrement=False)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    service_area = Column(VARCHAR(191), nullable=False, autoincrement=False)
    main_pipe_flow_rate = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    main_pipe_leak_count = Column(INTEGER, nullable=False, autoincrement=False)
    service_line_flow_rate = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    service_line_leak_count = Column(INTEGER, nullable=False, autoincrement=False)
    service_connection_flow_rate = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    service_connection_leak_count = Column(INTEGER, nullable=False, autoincrement=False)
    valve_flow_rate = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    valve_leak_count = Column(INTEGER, nullable=False, autoincrement=False)
    hydrant_flow_rate = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    hydrant_leak_count = Column(INTEGER, nullable=False, autoincrement=False)
    meter_flow_rate = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    meter_leak_count = Column(INTEGER, nullable=False, autoincrement=False)
    curb_stop_flow_rate = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    curb_stop_leak_count = Column(INTEGER, nullable=False, autoincrement=False)
    total_flow = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
