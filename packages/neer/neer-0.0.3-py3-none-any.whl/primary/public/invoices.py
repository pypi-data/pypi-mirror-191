from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Invoices(PrimaryBase):
    __tablename__ = 'invoices'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER, autoincrement=False)
    team_id = Column(INTEGER, autoincrement=False)
    provider_id = Column(VARCHAR(191), nullable=False, autoincrement=False)
    total = Column(NUMERIC(8, 2), autoincrement=False)
    tax = Column(NUMERIC(8, 2), autoincrement=False)
    card_country = Column(VARCHAR(191), autoincrement=False)
    billing_state = Column(VARCHAR(191), autoincrement=False)
    billing_zip = Column(VARCHAR(191), autoincrement=False)
    billing_country = Column(VARCHAR(191), autoincrement=False)
    vat_id = Column(VARCHAR(50), autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
