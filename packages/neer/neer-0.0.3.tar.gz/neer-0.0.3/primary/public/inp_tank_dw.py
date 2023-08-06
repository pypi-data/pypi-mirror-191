from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpTankDw(PrimaryBase):
    __tablename__ = 'inp_tank_dw'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(250), autoincrement=False)
    descript = Column(VARCHAR(1024), autoincrement=False)
    elevation = Column(VARCHAR(25), autoincrement=False)
    init_level = Column(VARCHAR(25), autoincrement=False)
    min_level = Column(VARCHAR(25), autoincrement=False)
    max_level = Column(VARCHAR(25), autoincrement=False)
    diameter = Column(VARCHAR(25), autoincrement=False)
    min_vol = Column(VARCHAR(25), autoincrement=False)
    vol_curve = Column(VARCHAR(25), autoincrement=False)
    mix_model = Column(VARCHAR(25), autoincrement=False)
    mix_fract = Column(VARCHAR(25), autoincrement=False)
    react_coef = Column(VARCHAR(25), autoincrement=False)
    init_qual = Column(VARCHAR(25), autoincrement=False)
    src_qual = Column(VARCHAR(25), autoincrement=False)
    src_pattern = Column(VARCHAR(25), autoincrement=False)
    src_type = Column(VARCHAR(25), autoincrement=False)
    project_id = Column(INTEGER, autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    a_type = Column(VARCHAR(191), autoincrement=False)
    a_status = Column(VARCHAR(191), autoincrement=False)
    a_pressure_zone = Column(VARCHAR(191), autoincrement=False)
    a_dma = Column(VARCHAR(191), autoincrement=False)
