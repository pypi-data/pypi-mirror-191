from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Migrations(PrimaryBase):
    __tablename__ = 'migrations'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    migration = Column(VARCHAR(191), nullable=False, autoincrement=False)
    batch = Column(INTEGER, nullable=False, autoincrement=False)
