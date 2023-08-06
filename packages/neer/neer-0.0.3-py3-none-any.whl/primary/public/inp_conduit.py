from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpConduit(PrimaryBase):
    __tablename__ = 'inp_conduit'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    inlet_node = Column(VARCHAR(250), autoincrement=False)
    outlet_node = Column(VARCHAR(250), autoincrement=False)
    length = Column(VARCHAR(25), autoincrement=False)
    mannin_n = Column(VARCHAR(25), autoincrement=False)
    inlet_height = Column(VARCHAR(25), autoincrement=False)
    outlet_height = Column(VARCHAR(25), autoincrement=False)
    init_flow = Column(VARCHAR(25), autoincrement=False)
    max_flow = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    mukey = Column(VARCHAR(191), autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    flow_10yr = Column(VARCHAR(191), autoincrement=False)
    flow_25yr = Column(VARCHAR(191), autoincrement=False)
    flow_50yr = Column(VARCHAR(191), autoincrement=False)
    flow_100yr = Column(VARCHAR(191), autoincrement=False)
    flow_500yr = Column(VARCHAR(191), autoincrement=False)
    flow_1000yr = Column(VARCHAR(191), autoincrement=False)
    flow_2000yr = Column(VARCHAR(191), autoincrement=False)
    flow_monitor = Column(VARCHAR(191), autoincrement=False)
    is_road = Column(INTEGER, autoincrement=False)
    location = Column(VARCHAR(191), autoincrement=False)
