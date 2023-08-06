from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class ProcessedCofTransportationRating(PrimaryBase):
    __tablename__ = 'processed_cof_transportation_rating'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    type = Column(VARCHAR(191), nullable=False, autoincrement=False)
    name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    rating = Column(TEXT, nullable=False, autoincrement=False)
    project_id = Column(INTEGER, autoincrement=False)
    simulation_id = Column(INTEGER, autoincrement=False)
