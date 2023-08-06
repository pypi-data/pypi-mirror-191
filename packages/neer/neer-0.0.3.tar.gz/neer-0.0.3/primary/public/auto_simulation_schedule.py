from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, SMALLINT
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class AutoSimulationSchedule(PrimaryBase):
    __tablename__ = 'auto_simulation_schedule'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(VARCHAR(191), autoincrement=False)
    repetition = Column(VARCHAR(191), autoincrement=False)
    time = Column(VARCHAR(191), autoincrement=False)
    start_date = Column(DATE, autoincrement=False)
    end_date = Column(DATE, autoincrement=False)
    forecast = Column(VARCHAR(191), autoincrement=False)
    hindcast = Column(VARCHAR(191), autoincrement=False)
    run_rainfall_event_analysis = Column(SMALLINT, autoincrement=False)
