from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpHydrographValues(PrimaryBase):
    __tablename__ = 'inp_hydrograph_values'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    inp_hydrograph_id = Column(BIGINT, nullable=False, autoincrement=False)
    rain_gage_month = Column(VARCHAR(20), nullable=False, autoincrement=False)
    response = Column(VARCHAR(20), nullable=False, autoincrement=False)
    r = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    t = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    k = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    dmax = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    drecov = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    dinit = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
