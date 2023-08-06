from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, JSON
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class NoaaFrequencyTables(PrimaryBase):
    __tablename__ = 'noaa_frequency_tables'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    volume = Column(INTEGER, nullable=False, autoincrement=False)
    version = Column(INTEGER, nullable=False, autoincrement=False)
    time_series_type = Column(VARCHAR(191), nullable=False, autoincrement=False)
    lat = Column(VARCHAR(191), nullable=False, autoincrement=False)
    long = Column(VARCHAR(191), nullable=False, autoincrement=False)
    upper_table = Column(JSON, autoincrement=False)
    lower_table = Column(JSON, autoincrement=False)
    mean_table = Column(JSON, autoincrement=False)
    upper_filepath = Column(VARCHAR(191), autoincrement=False)
    lower_filepath = Column(VARCHAR(191), autoincrement=False)
    mean_filepath = Column(VARCHAR(191), autoincrement=False)
