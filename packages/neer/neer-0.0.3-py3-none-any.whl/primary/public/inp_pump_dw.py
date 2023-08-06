from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpPumpDw(PrimaryBase):
    __tablename__ = 'inp_pump_dw'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(250), autoincrement=False)
    inlet_node = Column(VARCHAR(250), autoincrement=False)
    outlet_node = Column(VARCHAR(250), autoincrement=False)
    descript = Column(VARCHAR(1024), autoincrement=False)
    pump_curve = Column(VARCHAR(25), autoincrement=False)
    power = Column(VARCHAR(25), autoincrement=False)
    speed = Column(VARCHAR(25), autoincrement=False)
    pattern = Column(VARCHAR(25), autoincrement=False)
    init_status = Column(VARCHAR(25), autoincrement=False)
    effic_curve = Column(VARCHAR(25), autoincrement=False)
    enrgy_price = Column(VARCHAR(25), autoincrement=False)
    price_pat = Column(VARCHAR(25), autoincrement=False)
    project_id = Column(INTEGER, autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    a_type = Column(VARCHAR(191), autoincrement=False)
    a_status = Column(VARCHAR(191), autoincrement=False)
    a_pressure_zone = Column(VARCHAR(191), autoincrement=False)
    a_dma = Column(VARCHAR(191), autoincrement=False)
