from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpHydrograph(PrimaryBase):
    __tablename__ = 'inp_hydrograph'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    rain_gage_name = Column(VARCHAR(250), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
