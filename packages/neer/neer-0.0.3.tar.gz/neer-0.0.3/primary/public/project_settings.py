from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class ProjectSettings(PrimaryBase):
    __tablename__ = 'project_settings'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    layer_settings = Column(TEXT, autoincrement=False)
    column_settings = Column(TEXT, autoincrement=False)
    user_id = Column(INTEGER, autoincrement=False)
