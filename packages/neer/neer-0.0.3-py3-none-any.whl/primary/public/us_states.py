from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class UsStates(PrimaryBase):
    __tablename__ = 'us_states'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    region = Column(INTEGER, autoincrement=False)
    division = Column(INTEGER, autoincrement=False)
    state_id = Column(INTEGER, autoincrement=False)
    statens = Column(INTEGER, autoincrement=False)
    stusps = Column(VARCHAR(10), autoincrement=False)
    name = Column(VARCHAR(255), autoincrement=False)
    lsad = Column(INTEGER, autoincrement=False)
    mtfcc = Column(VARCHAR(255), autoincrement=False)
    funcstat = Column(VARCHAR(255), autoincrement=False)
    aland = Column(BIGINT, autoincrement=False)
    awater = Column(BIGINT, autoincrement=False)
    intptlat = Column(VARCHAR(255), autoincrement=False)
    intptlon = Column(VARCHAR(255), autoincrement=False)
