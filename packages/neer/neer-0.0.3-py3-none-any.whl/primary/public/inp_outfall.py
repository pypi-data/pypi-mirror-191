from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpOutfall(PrimaryBase):
    __tablename__ = 'inp_outfall'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    invert_elev = Column(VARCHAR(25), autoincrement=False)
    outfall_type = Column(VARCHAR(25), autoincrement=False)
    stage_table_time_series = Column(VARCHAR(191), autoincrement=False)
    tide_gate = Column(VARCHAR(25), autoincrement=False)
    route_to = Column(VARCHAR(100), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    mukey = Column(VARCHAR(191), autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    back_test_outfall_type = Column(VARCHAR(191), autoincrement=False)
    back_test_stage_table_time_series = Column(VARCHAR(191), autoincrement=False)
