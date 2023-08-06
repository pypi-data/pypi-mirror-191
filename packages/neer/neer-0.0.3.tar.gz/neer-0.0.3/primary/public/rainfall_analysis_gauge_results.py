from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class RainfallAnalysisGaugeResults(PrimaryBase):
    __tablename__ = 'rainfall_analysis_gauge_results'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    rainfall_analysis_gauge_id = Column(INTEGER, nullable=False, autoincrement=False)
    start_date_time = Column(TIMESTAMP, nullable=False, autoincrement=False)
    end_date_time = Column(TIMESTAMP, nullable=False, autoincrement=False)
    duration = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    max_rainfall = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    min_rainfall = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    mean_rainfall = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    total_rainfall_volume = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    rainfall_period = Column(VARCHAR(191), autoincrement=False)
