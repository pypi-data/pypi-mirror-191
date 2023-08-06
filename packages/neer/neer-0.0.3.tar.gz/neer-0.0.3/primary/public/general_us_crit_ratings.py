from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class GeneralUsCritRatings(PrimaryBase):
    __tablename__ = 'general_us_crit_ratings'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    facility = Column(VARCHAR(255), autoincrement=False)
    rating = Column(INTEGER, autoincrement=False)
