from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class ProcessedCofFacilityDistance(PrimaryBase):
    __tablename__ = 'processed_cof_facility_distance'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    object_name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    object_type = Column(VARCHAR(191), nullable=False, autoincrement=False)
    facility_name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    facility_type = Column(VARCHAR(191), nullable=False, autoincrement=False)
    asset_type = Column(VARCHAR(191), autoincrement=False)
    distance = Column(TEXT, autoincrement=False)
    is_under = Column(VARCHAR(191), autoincrement=False)
    is_near = Column(VARCHAR(191), autoincrement=False)
    project_id = Column(INTEGER, autoincrement=False)
    simulation_id = Column(INTEGER, autoincrement=False)
