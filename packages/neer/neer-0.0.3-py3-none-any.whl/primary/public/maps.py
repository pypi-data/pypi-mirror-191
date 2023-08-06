from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Maps(PrimaryBase):
    __tablename__ = 'maps'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(50), autoincrement=False)
    name = Column(VARCHAR(50), autoincrement=False)
    center_lat = Column(VARCHAR(30), autoincrement=False)
    center_lng = Column(VARCHAR(30), autoincrement=False)
    zoom_level = Column(VARCHAR(30), autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
