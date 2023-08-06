from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class SpatialRefSys(PrimaryBase):
    __tablename__ = 'spatial_ref_sys'
    __table_args__ = {'schema': 'public'}
    
    srid = Column(INTEGER, primary_key=True, autoincrement=False)
    auth_name = Column(VARCHAR(256), autoincrement=False)
    auth_srid = Column(INTEGER, autoincrement=False)
    srtext = Column(VARCHAR(2048), autoincrement=False)
    proj4text = Column(VARCHAR(2048), autoincrement=False)
