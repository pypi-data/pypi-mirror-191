from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class CalibrationDataDw(PrimaryBase):
    __tablename__ = 'calibration_data_dw'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    calibration_type = Column(VARCHAR(50), nullable=False, autoincrement=False)
    object_name = Column(VARCHAR(50), nullable=False, autoincrement=False)
    value = Column(NUMERIC(8, 2), autoincrement=False)
    date = Column(DATE, autoincrement=False)
    time = Column(TIME, autoincrement=False)
