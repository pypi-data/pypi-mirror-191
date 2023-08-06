from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class DiscountRequests(PrimaryBase):
    __tablename__ = 'discount_requests'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    email = Column(TEXT, nullable=False, autoincrement=False)
    reason = Column(TEXT, nullable=False, autoincrement=False)
    status = Column(TEXT, autoincrement=False)
    coupon = Column(TEXT, autoincrement=False)
    sent_at = Column(TIMESTAMP, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
