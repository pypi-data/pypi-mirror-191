from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class FeatureStations(PrimaryBase):
    __tablename__ = 'feature_stations'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(VARCHAR(191), autoincrement=False)
    name = Column(VARCHAR(191), autoincrement=False)
    type = Column(VARCHAR(191), autoincrement=False)
    sensor_id = Column(VARCHAR(191), autoincrement=False)
    adjustment = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
