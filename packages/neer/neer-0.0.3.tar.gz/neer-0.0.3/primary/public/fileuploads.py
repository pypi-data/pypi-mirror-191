from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Fileuploads(PrimaryBase):
    __tablename__ = 'fileuploads'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    filename = Column(VARCHAR(191), nullable=False, autoincrement=False)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    user_id = Column(INTEGER, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
