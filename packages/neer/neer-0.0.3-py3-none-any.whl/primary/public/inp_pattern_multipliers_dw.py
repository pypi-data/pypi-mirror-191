from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, SMALLINT
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpPatternMultipliersDw(PrimaryBase):
    __tablename__ = 'inp_pattern_multipliers_dw'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    inp_pattern_dw_id = Column(INTEGER, nullable=False, autoincrement=False)
    order = Column(SMALLINT, nullable=False, autoincrement=False)
    value = Column(DOUBLE_PRECISION, autoincrement=False)
