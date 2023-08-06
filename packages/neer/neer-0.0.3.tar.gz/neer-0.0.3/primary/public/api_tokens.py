from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT, SMALLINT
from base import PrimaryBase

class ApiTokens(PrimaryBase):
    __tablename__ = 'api_tokens'
    __table_args__ = {'schema': 'public'}
    
    id = Column(VARCHAR(191), primary_key=True, autoincrement=False)
    user_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    token = Column(VARCHAR(100), nullable=False, autoincrement=False)
    meta = Column('metadata', TEXT, nullable=False, autoincrement=False)
    transient = Column(SMALLINT, nullable=False, autoincrement=False)
    last_used_at = Column(TIMESTAMP, autoincrement=False)
    expires_at = Column(TIMESTAMP, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
