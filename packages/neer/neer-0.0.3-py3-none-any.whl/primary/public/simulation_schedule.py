from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SimulationSchedule(PrimaryBase):
    __tablename__ = 'simulation_schedule'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(VARCHAR(191), autoincrement=False)
    date = Column(VARCHAR(191), autoincrement=False)
    time = Column(VARCHAR(191), autoincrement=False)
    repetition = Column(VARCHAR(191), autoincrement=False)
    user_id = Column(VARCHAR(191), autoincrement=False)
