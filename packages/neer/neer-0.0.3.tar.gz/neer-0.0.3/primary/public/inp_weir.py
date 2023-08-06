from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class InpWeir(PrimaryBase):
    __tablename__ = 'inp_weir'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(VARCHAR(250), autoincrement=False)
    from_node = Column(VARCHAR(250), autoincrement=False)
    to_node = Column(VARCHAR(250), autoincrement=False)
    type = Column(VARCHAR(25), autoincrement=False)
    crest_ht = Column(VARCHAR(25), autoincrement=False)
    q_coeff = Column(VARCHAR(25), autoincrement=False)
    gated = Column(VARCHAR(25), autoincrement=False)
    end_con = Column(VARCHAR(25), autoincrement=False)
    end_coeff = Column(VARCHAR(25), autoincrement=False)
    surcharge = Column(VARCHAR(25), autoincrement=False)
    road_width = Column(VARCHAR(25), autoincrement=False)
    road_surf = Column(VARCHAR(25), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
    coeff_curve = Column(VARCHAR(50), autoincrement=False)
    mukey = Column(VARCHAR(191), autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    is_road = Column(INTEGER, autoincrement=False)
    location = Column(VARCHAR(191), autoincrement=False)
