from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpDivider(PrimaryBase):
    __tablename__ = 'inp_divider'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    elev = Column(DOUBLE_PRECISION, nullable=False, autoincrement=False)
    div_link = Column(VARCHAR(75), autoincrement=False)
    type = Column(VARCHAR(20), nullable=False, autoincrement=False)
    q_min = Column(DOUBLE_PRECISION, autoincrement=False)
    d_curve = Column(VARCHAR(75), autoincrement=False)
    ht = Column(DOUBLE_PRECISION, autoincrement=False)
    cd = Column(DOUBLE_PRECISION, autoincrement=False)
    y_max = Column(DOUBLE_PRECISION, autoincrement=False)
    y0 = Column(DOUBLE_PRECISION, autoincrement=False)
    y_sur = Column(DOUBLE_PRECISION, autoincrement=False)
    apond = Column(DOUBLE_PRECISION, autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    mukey = Column(VARCHAR(191), autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
