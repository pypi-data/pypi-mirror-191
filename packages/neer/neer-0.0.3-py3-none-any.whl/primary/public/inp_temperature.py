from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpTemperature(PrimaryBase):
    __tablename__ = 'inp_temperature'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    data_type = Column(VARCHAR(30), autoincrement=False)
    file_name = Column(VARCHAR(255), autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    start_reading_at = Column(VARCHAR(25), autoincrement=False)
