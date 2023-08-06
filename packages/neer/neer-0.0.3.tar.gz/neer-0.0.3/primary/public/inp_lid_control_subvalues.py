from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, SMALLINT
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpLidControlSubvalues(PrimaryBase):
    __tablename__ = 'inp_lid_control_subvalues'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    inp_lid_control_value_id = Column(BIGINT, nullable=False, autoincrement=False)
    parameter_number = Column(SMALLINT, nullable=False, autoincrement=False)
    value = Column(VARCHAR(50), nullable=False, autoincrement=False)
