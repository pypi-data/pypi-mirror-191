from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpPipeDw(PrimaryBase):
    __tablename__ = 'inp_pipe_dw'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(250), autoincrement=False)
    inlet_node = Column(VARCHAR(250), autoincrement=False)
    outlet_node = Column(VARCHAR(250), autoincrement=False)
    descript = Column(VARCHAR(1024), autoincrement=False)
    length = Column(VARCHAR(25), autoincrement=False)
    diameter = Column(VARCHAR(25), autoincrement=False)
    roughness = Column(VARCHAR(25), autoincrement=False)
    loss_coef = Column(VARCHAR(25), autoincrement=False)
    init_status = Column(VARCHAR(25), autoincrement=False)
    bulk_coef = Column(VARCHAR(25), autoincrement=False)
    wall_coef = Column(VARCHAR(25), autoincrement=False)
    project_id = Column(INTEGER, autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    a_type = Column(VARCHAR(191), autoincrement=False)
    a_status = Column(VARCHAR(191), autoincrement=False)
    a_pressure_zone = Column(VARCHAR(191), autoincrement=False)
    a_dma = Column(VARCHAR(191), autoincrement=False)
