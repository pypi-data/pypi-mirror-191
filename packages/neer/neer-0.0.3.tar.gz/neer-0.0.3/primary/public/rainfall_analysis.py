from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class RainfallAnalysis(PrimaryBase):
    __tablename__ = 'rainfall_analysis'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    group = Column(VARCHAR(191), nullable=False, autoincrement=False)
    min_interevent = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    event_threshold = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    extend_event_preceeding = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    extend_event_following = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    limit_event_from = Column(TIMESTAMP, autoincrement=False)
    limit_event_to = Column(TIMESTAMP, autoincrement=False)
    exclude_audit_exceptions = Column(BOOLEAN, nullable=False, autoincrement=False)
    clear_existing_events = Column(BOOLEAN, nullable=False, autoincrement=False)
    noaa_atlas_14_frequency_events = Column(BOOLEAN, nullable=False, autoincrement=False)
    auto_simulation = Column(BOOLEAN, nullable=False, autoincrement=False)
    perform_forecasted_rainfall_event_analysis = Column(BOOLEAN, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
