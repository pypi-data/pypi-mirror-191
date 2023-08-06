from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, ARRAY
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Clients(PrimaryBase):
    __tablename__ = 'clients'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    parent_id = Column(INTEGER, autoincrement=False)
    slug = Column(TEXT, nullable=False, autoincrement=False)
    name = Column(TEXT, nullable=False, autoincrement=False)
    description = Column(TEXT, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    aliases = Column(ARRAY(TEXT), nullable=False, autoincrement=False)
