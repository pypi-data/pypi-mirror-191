from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class CustomerSurveyForm(PrimaryBase):
    __tablename__ = 'customer_survey_form'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    account_number = Column(VARCHAR(191), nullable=False, autoincrement=False)
    project_id = Column(INTEGER, autoincrement=False)
    first_name = Column(VARCHAR(191), autoincrement=False)
    last_name = Column(VARCHAR(191), autoincrement=False)
    phone = Column(VARCHAR(25), autoincrement=False)
    email = Column(VARCHAR(191), autoincrement=False)
    address = Column(VARCHAR(500), autoincrement=False)
    occupancy_type = Column(VARCHAR(10), autoincrement=False)
    material = Column(VARCHAR(191), autoincrement=False)
    installation_date = Column(DATE, autoincrement=False)
    source_of_info = Column(VARCHAR(191), autoincrement=False)
    photo = Column(TEXT, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
