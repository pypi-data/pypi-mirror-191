from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class LandUseCodeScores(PrimaryBase):
    __tablename__ = 'land_use_code_scores'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    lu_code = Column(INTEGER, autoincrement=False)
    lu_score = Column(INTEGER, autoincrement=False)
    name_type = Column(VARCHAR(200), autoincrement=False)
    description = Column(TEXT, autoincrement=False)
