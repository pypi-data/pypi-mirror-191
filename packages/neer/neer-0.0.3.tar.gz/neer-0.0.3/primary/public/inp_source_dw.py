from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpSourceDw(PrimaryBase):
    __tablename__ = 'inp_source_dw'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    type = Column(VARCHAR(25), autoincrement=False)
    quality = Column(DOUBLE_PRECISION, autoincrement=False)
    pattern = Column(VARCHAR(191), autoincrement=False)
    description = Column(TEXT, autoincrement=False)
