from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpJunction(PrimaryBase):
    __tablename__ = 'inp_junction'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    invert_elev = Column(VARCHAR(25), autoincrement=False)
    max_depth = Column(VARCHAR(25), autoincrement=False)
    init_depth = Column(VARCHAR(25), autoincrement=False)
    surcharge_depth = Column(VARCHAR(25), autoincrement=False)
    ponded_area = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    mukey = Column(VARCHAR(191), autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    wse_10yr = Column(VARCHAR(191), autoincrement=False)
    wse_25yr = Column(VARCHAR(191), autoincrement=False)
    wse_50yr = Column(VARCHAR(191), autoincrement=False)
    wse_100yr = Column(VARCHAR(191), autoincrement=False)
    wse_500yr = Column(VARCHAR(191), autoincrement=False)
    wse_1000yr = Column(VARCHAR(191), autoincrement=False)
    wse_2000yr = Column(VARCHAR(191), autoincrement=False)
    wse_monitor = Column(VARCHAR(191), autoincrement=False)
    stage_10yr = Column(VARCHAR(191), autoincrement=False)
    stage_25yr = Column(VARCHAR(191), autoincrement=False)
    stage_50yr = Column(VARCHAR(191), autoincrement=False)
    stage_100yr = Column(VARCHAR(191), autoincrement=False)
    stage_500yr = Column(VARCHAR(191), autoincrement=False)
    stage_1000yr = Column(VARCHAR(191), autoincrement=False)
    stage_2000yr = Column(VARCHAR(191), autoincrement=False)
    stage_monitor = Column(VARCHAR(191), autoincrement=False)
    back_test_init_depth = Column(VARCHAR(191), autoincrement=False)
