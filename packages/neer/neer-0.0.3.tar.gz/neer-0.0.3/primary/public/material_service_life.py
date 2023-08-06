from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class MaterialServiceLife(PrimaryBase):
    __tablename__ = 'material_service_life'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    material = Column(VARCHAR, autoincrement=False)
    service_life_years = Column(INTEGER, autoincrement=False)
    project_type = Column(VARCHAR, autoincrement=False)
    structure_type = Column(VARCHAR, autoincrement=False)
    structure_details = Column(VARCHAR, autoincrement=False)
