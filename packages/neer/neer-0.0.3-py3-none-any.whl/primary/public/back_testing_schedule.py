from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, JSON
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class BackTestingSchedule(PrimaryBase):
    __tablename__ = 'back_testing_schedule'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(VARCHAR(191), autoincrement=False)
    repetition = Column(VARCHAR(191), autoincrement=False)
    time = Column(VARCHAR(191), autoincrement=False)
    start_date = Column(VARCHAR(191), autoincrement=False)
    end_date = Column(VARCHAR(191), autoincrement=False)
    forecast = Column(VARCHAR(191), autoincrement=False)
    hindcast = Column(VARCHAR(191), autoincrement=False)
    simulation_id = Column(VARCHAR(191), autoincrement=False)
    simulation_queue = Column(JSON, autoincrement=False)
