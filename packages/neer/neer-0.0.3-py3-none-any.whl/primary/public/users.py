from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, SMALLINT
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Users(PrimaryBase):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    email = Column(VARCHAR(191), nullable=False, autoincrement=False)
    email_verified_at = Column(TIMESTAMP, autoincrement=False)
    password = Column(VARCHAR(191), nullable=False, autoincrement=False)
    remember_token = Column(VARCHAR(100), autoincrement=False)
    photo_url = Column(TEXT, autoincrement=False)
    uses_two_factor_auth = Column(SMALLINT, nullable=False, autoincrement=False)
    authy_id = Column(VARCHAR(191), autoincrement=False)
    country_code = Column(VARCHAR(10), autoincrement=False)
    phone = Column(VARCHAR(25), autoincrement=False)
    two_factor_reset_code = Column(VARCHAR(100), autoincrement=False)
    current_team_id = Column(INTEGER, autoincrement=False)
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
    last_read_announcements_at = Column(TIMESTAMP, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    progress = Column(VARCHAR(191), autoincrement=False)
    api_secret = Column(TEXT, autoincrement=False)
    preferred_timezone = Column(VARCHAR(191), autoincrement=False)
    session_id = Column(TEXT, autoincrement=False)
    preferences = Column(TEXT, autoincrement=False)
