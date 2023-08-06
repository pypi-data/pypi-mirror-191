from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpTransectsNc(PrimaryBase):
    __tablename__ = 'inp_transects_nc'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    transects_id = Column(INTEGER, nullable=False, autoincrement=False)
    n_left = Column(VARCHAR(191), autoincrement=False)
    n_right = Column(VARCHAR(191), autoincrement=False)
    n_chan1 = Column(VARCHAR(191), autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
