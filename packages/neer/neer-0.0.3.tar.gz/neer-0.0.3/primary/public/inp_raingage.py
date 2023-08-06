from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpRaingage(PrimaryBase):
    __tablename__ = 'inp_raingage'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    rain_type = Column(VARCHAR(25), autoincrement=False)
    recd_freq = Column(VARCHAR(25), autoincrement=False)
    snow_catch = Column(VARCHAR(25), autoincrement=False)
    data_source = Column(VARCHAR(25), autoincrement=False)
    source_name = Column(VARCHAR(255), autoincrement=False)
    station_id = Column(VARCHAR(250), autoincrement=False)
    rain_units = Column(VARCHAR(25), autoincrement=False)
    t_series = Column(VARCHAR(250), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    back_test_source_name = Column(VARCHAR(191), autoincrement=False)
    virtual_or_local = Column(VARCHAR(191), nullable=False, autoincrement=False)
