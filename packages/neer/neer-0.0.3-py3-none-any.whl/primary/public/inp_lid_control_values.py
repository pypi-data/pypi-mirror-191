from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpLidControlValues(PrimaryBase):
    __tablename__ = 'inp_lid_control_values'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    inp_lid_control_id = Column(BIGINT, nullable=False, autoincrement=False)
    type = Column(VARCHAR(20), nullable=False, autoincrement=False)
