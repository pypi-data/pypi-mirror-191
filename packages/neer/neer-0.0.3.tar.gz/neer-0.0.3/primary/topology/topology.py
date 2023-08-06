from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Topology(PrimaryBase):
    __tablename__ = 'topology'
    __table_args__ = {'schema': 'topology'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False, autoincrement=False)
    srid = Column(INTEGER, nullable=False, autoincrement=False)
    precision = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    hasz = Column(BOOLEAN, nullable=False, autoincrement=False)
