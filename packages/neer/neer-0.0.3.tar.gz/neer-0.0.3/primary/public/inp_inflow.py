from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpInflow(PrimaryBase):
    __tablename__ = 'inp_inflow'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    node = Column(VARCHAR(250), autoincrement=False)
    parameter = Column(VARCHAR(25), autoincrement=False)
    time_series = Column(VARCHAR(25), autoincrement=False)
    type = Column(VARCHAR(25), autoincrement=False)
    m_factor = Column(VARCHAR(25), autoincrement=False)
    s_factor = Column(VARCHAR(25), autoincrement=False)
    baseline = Column(VARCHAR(25), autoincrement=False)
    pattern = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
