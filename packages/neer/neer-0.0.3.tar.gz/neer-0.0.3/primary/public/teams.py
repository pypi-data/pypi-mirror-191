from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Teams(PrimaryBase):
    __tablename__ = 'teams'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    owner_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    slug = Column(VARCHAR(191), autoincrement=False)
    photo_url = Column(TEXT, autoincrement=False)
    stripe_id = Column(VARCHAR(191), autoincrement=False)
    current_billing_plan = Column(VARCHAR(191), autoincrement=False)
    card_brand = Column(VARCHAR(191), autoincrement=False)
    card_last_four = Column(VARCHAR(191), autoincrement=False)
    card_country = Column(VARCHAR(191), autoincrement=False)
    billing_address = Column(VARCHAR(191), autoincrement=False)
    billing_address_line_2 = Column(VARCHAR(191), autoincrement=False)
    billing_city = Column(VARCHAR(191), autoincrement=False)
    billing_state = Column(VARCHAR(191), autoincrement=False)
    billing_zip = Column(VARCHAR(25), autoincrement=False)
    billing_country = Column(VARCHAR(2), autoincrement=False)
    vat_id = Column(VARCHAR(50), autoincrement=False)
    extra_billing_information = Column(TEXT, autoincrement=False)
    trial_ends_at = Column(TIMESTAMP, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    client_name = Column(TEXT, autoincrement=False)
    api_secret = Column(TEXT, autoincrement=False)
