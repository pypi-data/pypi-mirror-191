from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpLosses(PrimaryBase):
    __tablename__ = 'inp_losses'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    conduit = Column(VARCHAR(250), autoincrement=False)
    k_entry = Column(VARCHAR(25), autoincrement=False)
    k_exit = Column(VARCHAR(25), autoincrement=False)
    k_avg = Column(VARCHAR(25), autoincrement=False)
    flap = Column(VARCHAR(25), autoincrement=False)
    seepage = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
