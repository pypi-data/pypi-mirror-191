from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class NonRevenueWaterLoss(PrimaryBase):
    __tablename__ = 'non_revenue_water_loss'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    unbilled_metered = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    unbilled_unmetered = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    real_loss = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    customer_metering = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    unauthorized_consumption = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    system_handling_error = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
