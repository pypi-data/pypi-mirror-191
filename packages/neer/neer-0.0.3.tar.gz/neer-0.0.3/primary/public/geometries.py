from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Geometries(PrimaryBase):
    __tablename__ = 'geometries'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    object_type = Column(VARCHAR(191), nullable=False, autoincrement=False)
    geometry = Column(TEXT, nullable=False, autoincrement=False)
