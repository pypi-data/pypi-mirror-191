from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Subscriptions(PrimaryBase):
    __tablename__ = 'subscriptions'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    stripe_id = Column(VARCHAR(191), nullable=False, autoincrement=False)
    stripe_plan = Column(VARCHAR(191), nullable=False, autoincrement=False)
    quantity = Column(INTEGER, nullable=False, autoincrement=False)
    trial_ends_at = Column(TIMESTAMP, autoincrement=False)
    ends_at = Column(TIMESTAMP, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    stripe_status = Column(VARCHAR(191), autoincrement=False)
