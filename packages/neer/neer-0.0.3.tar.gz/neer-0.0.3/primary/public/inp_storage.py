from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, SMALLINT
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpStorage(PrimaryBase):
    __tablename__ = 'inp_storage'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    invert_elev = Column(VARCHAR(25), autoincrement=False)
    max_depth = Column(VARCHAR(25), autoincrement=False)
    init_depth = Column(VARCHAR(25), autoincrement=False)
    type = Column(VARCHAR(25), autoincrement=False)
    a_curve = Column(VARCHAR(75), autoincrement=False)
    a1 = Column(DOUBLE_PRECISION, autoincrement=False)
    a2 = Column(DOUBLE_PRECISION, autoincrement=False)
    a0 = Column(DOUBLE_PRECISION, autoincrement=False)
    apond = Column(SMALLINT, autoincrement=False)
    f_evap = Column(DOUBLE_PRECISION, autoincrement=False)
    psi = Column(DOUBLE_PRECISION, autoincrement=False)
    ksat = Column(DOUBLE_PRECISION, autoincrement=False)
    imd = Column(DOUBLE_PRECISION, autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    mukey = Column(VARCHAR(191), autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    storage_holding_capacity = Column(DOUBLE_PRECISION, autoincrement=False)
    storage_type = Column(VARCHAR(191), autoincrement=False)
