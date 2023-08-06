from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class TeamModels(PrimaryBase):
    __tablename__ = 'team_models'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    team_id = Column(INTEGER, nullable=False, autoincrement=False)
    model_id = Column(INTEGER, nullable=False, autoincrement=False)
