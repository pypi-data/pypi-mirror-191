from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpRdii(PrimaryBase):
    __tablename__ = 'inp_rdii'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    node = Column(VARCHAR(250), autoincrement=False)
    uh_group = Column(VARCHAR(25), autoincrement=False)
    sewer_area = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
