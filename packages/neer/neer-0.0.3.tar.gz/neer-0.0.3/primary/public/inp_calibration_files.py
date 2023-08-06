from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpCalibrationFiles(PrimaryBase):
    __tablename__ = 'inp_calibration_files'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    calibration_type = Column(VARCHAR(50), autoincrement=False)
    calibration_file = Column(VARCHAR(100), autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    adjustment = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
