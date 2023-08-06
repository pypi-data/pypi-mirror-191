from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Invitations(PrimaryBase):
    __tablename__ = 'invitations'
    __table_args__ = {'schema': 'public'}
    
    id = Column(VARCHAR(191), primary_key=True, autoincrement=False)
    team_id = Column(INTEGER, nullable=False, autoincrement=False)
    user_id = Column(INTEGER, autoincrement=False)
    role = Column(VARCHAR(191), autoincrement=False)
    email = Column(VARCHAR(191), nullable=False, autoincrement=False)
    token = Column(VARCHAR(40), nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
