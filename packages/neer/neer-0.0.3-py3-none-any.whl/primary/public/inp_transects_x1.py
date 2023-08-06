from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpTransectsX1(PrimaryBase):
    __tablename__ = 'inp_transects_x1'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    transects_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    n_sta = Column(VARCHAR(191), autoincrement=False)
    x_left = Column(VARCHAR(191), autoincrement=False)
    x_right = Column(VARCHAR(191), autoincrement=False)
    p1 = Column(VARCHAR(191), autoincrement=False)
    p2 = Column(VARCHAR(191), autoincrement=False)
    p3 = Column(VARCHAR(191), autoincrement=False)
    l_factor = Column(VARCHAR(191), autoincrement=False)
    w_factor = Column(VARCHAR(191), autoincrement=False)
    e_offset = Column(VARCHAR(191), autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
