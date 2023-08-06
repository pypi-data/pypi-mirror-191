from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpLidUsage(PrimaryBase):
    __tablename__ = 'inp_lid_usage'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    subcatchment = Column(VARCHAR(250), autoincrement=False)
    lid_process = Column(VARCHAR(50), nullable=False, autoincrement=False)
    number = Column(DOUBLE_PRECISION, autoincrement=False)
    area = Column(DOUBLE_PRECISION, autoincrement=False)
    width = Column(DOUBLE_PRECISION, autoincrement=False)
    init_satur = Column(DOUBLE_PRECISION, autoincrement=False)
    from_imp = Column(DOUBLE_PRECISION, autoincrement=False)
    to_perv = Column(INTEGER, autoincrement=False)
    report_file = Column(VARCHAR(191), autoincrement=False)
    drain_to = Column(VARCHAR(191), autoincrement=False)
    from_perv = Column(VARCHAR(191), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
