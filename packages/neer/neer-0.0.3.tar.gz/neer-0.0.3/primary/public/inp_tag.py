from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpTag(PrimaryBase):
    __tablename__ = 'inp_tag'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    item_type = Column(VARCHAR(100), autoincrement=False)
    item_name = Column(VARCHAR(100), autoincrement=False)
    tag = Column(VARCHAR(100), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
