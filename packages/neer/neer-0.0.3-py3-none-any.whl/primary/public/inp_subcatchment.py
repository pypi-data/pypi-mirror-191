from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpSubcatchment(PrimaryBase):
    __tablename__ = 'inp_subcatchment'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    raingage = Column(VARCHAR(50), autoincrement=False)
    outlet = Column(VARCHAR(50), autoincrement=False)
    total_area = Column(DOUBLE_PRECISION, autoincrement=False)
    pcnt_imperv = Column(DOUBLE_PRECISION, autoincrement=False)
    width = Column(DOUBLE_PRECISION, autoincrement=False)
    pcnt_slope = Column(DOUBLE_PRECISION, autoincrement=False)
    curb_length = Column(DOUBLE_PRECISION, autoincrement=False)
    snow_pack = Column(VARCHAR(50), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    mukey = Column(VARCHAR(191), autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
