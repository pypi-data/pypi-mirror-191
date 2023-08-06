from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class UserProjectMappingOld(PrimaryBase):
    __tablename__ = 'user_project_mapping_old'
    __table_args__ = {'schema': 'public'}
    
    user_project_mapping = Column(INTEGER, primary_key=True, autoincrement=False)
    user_id = Column(INTEGER, nullable=False, autoincrement=False)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
