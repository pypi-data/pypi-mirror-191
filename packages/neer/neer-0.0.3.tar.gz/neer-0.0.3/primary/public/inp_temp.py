from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpTemp(PrimaryBase):
    __tablename__ = 'inp_temp'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    time_series = Column(VARCHAR(250), autoincrement=False)
    file = Column(VARCHAR(25), autoincrement=False)
    windspeed = Column(VARCHAR(25), autoincrement=False)
    _monthly = Column(VARCHAR(25), autoincrement=False)
    windspeed_file = Column(VARCHAR(25), autoincrement=False)
    snowmelt = Column(VARCHAR(25), autoincrement=False)
    adc_impervious = Column(VARCHAR(25), autoincrement=False)
    adc_pervious = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
