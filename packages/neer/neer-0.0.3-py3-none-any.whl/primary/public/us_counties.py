from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class UsCounties(PrimaryBase):
    __tablename__ = 'us_counties'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    geo_id = Column(TEXT, autoincrement=False)
    county_name = Column(TEXT, autoincrement=False)
    namelsad = Column(TEXT, autoincrement=False)
    state_id = Column(INTEGER, autoincrement=False)
