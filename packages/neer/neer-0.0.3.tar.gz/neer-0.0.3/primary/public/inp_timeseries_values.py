from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpTimeseriesValues(PrimaryBase):
    __tablename__ = 'inp_timeseries_values'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    inp_timeseries_id = Column(BIGINT, nullable=False, autoincrement=False)
    date = Column(DATE, autoincrement=False)
    time = Column(VARCHAR(20), nullable=False, autoincrement=False)
    value = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
