from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class PerformanceIndicators(PrimaryBase):
    __tablename__ = 'performance_indicators'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    monthly_recurring_revenue = Column(NUMERIC(8, 2), nullable=False, autoincrement=False)
    yearly_recurring_revenue = Column(NUMERIC(8, 2), nullable=False, autoincrement=False)
    daily_volume = Column(NUMERIC(8, 2), nullable=False, autoincrement=False)
    new_users = Column(INTEGER, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
