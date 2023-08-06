from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, SMALLINT
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Notifications(PrimaryBase):
    __tablename__ = 'notifications'
    __table_args__ = {'schema': 'public'}
    
    id = Column(VARCHAR(191), primary_key=True, autoincrement=False)
    user_id = Column(INTEGER, nullable=False, autoincrement=False)
    created_by = Column(INTEGER, autoincrement=False)
    icon = Column(VARCHAR(50), autoincrement=False)
    body = Column(TEXT, nullable=False, autoincrement=False)
    action_text = Column(VARCHAR(191), autoincrement=False)
    action_url = Column(TEXT, autoincrement=False)
    read = Column(SMALLINT, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
