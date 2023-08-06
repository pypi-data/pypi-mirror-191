from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class CofModels(PrimaryBase):
    __tablename__ = 'cof_models'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    description = Column(TEXT, autoincrement=False)
    type = Column(VARCHAR(191), nullable=False, autoincrement=False)
    path = Column(VARCHAR(191), nullable=False, autoincrement=False)
    is_generic = Column(INTEGER, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
