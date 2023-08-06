from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class TeamUsers(PrimaryBase):
    __tablename__ = 'team_users'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    team_id = Column(INTEGER, nullable=False, autoincrement=False)
    user_id = Column(INTEGER, nullable=False, autoincrement=False)
    role = Column(VARCHAR(20), nullable=False, autoincrement=False)
