from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class PasswordResets(PrimaryBase):
    __tablename__ = 'password_resets'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    email = Column(VARCHAR(191), nullable=False, autoincrement=False)
    token = Column(VARCHAR(191), nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
