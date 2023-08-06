from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpPattern(PrimaryBase):
    __tablename__ = 'inp_pattern'
    __table_args__ = {'schema': 'public'}
    
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    type = Column(VARCHAR(50), autoincrement=False)
    description = Column(TEXT, autoincrement=False)
    multipliers = Column(VARCHAR(8000), autoincrement=False)
    id = Column(INTEGER, primary_key=True, autoincrement=True)
