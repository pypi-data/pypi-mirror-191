from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class WaterBalance(PrimaryBase):
    __tablename__ = 'water_balance'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    total_water_supplied = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    water_consumed_authorized = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    total_water_lost = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
