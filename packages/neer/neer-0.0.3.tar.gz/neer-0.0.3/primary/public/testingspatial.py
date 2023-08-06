from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Testingspatial(PrimaryBase):
    __tablename__ = 'testingspatial'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    id = Column(INTEGER, nullable=False, autoincrement=True)
    name = Column(VARCHAR, autoincrement=False)
    geom = Column(TEXT, autoincrement=False)
    geom2 = Column(TEXT, autoincrement=False)
    geom3 = Column(TEXT, autoincrement=False)
