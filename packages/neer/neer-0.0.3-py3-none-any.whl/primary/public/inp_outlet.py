from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpOutlet(PrimaryBase):
    __tablename__ = 'inp_outlet'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    node1 = Column(VARCHAR(250), autoincrement=False)
    node2 = Column(VARCHAR(250), autoincrement=False)
    offset = Column(DOUBLE_PRECISION, autoincrement=False)
    type = Column(VARCHAR(50), autoincrement=False)
    qcurve = Column(VARCHAR(50), autoincrement=False)
    coeff1 = Column(DOUBLE_PRECISION, autoincrement=False)
    coeff2 = Column(DOUBLE_PRECISION, autoincrement=False)
    gated = Column(VARCHAR(10), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    mukey = Column(VARCHAR(191), autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    is_road = Column(INTEGER, autoincrement=False)
    location = Column(VARCHAR(191), autoincrement=False)
