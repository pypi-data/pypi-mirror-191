from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class Layer(PrimaryBase):
    __tablename__ = 'layer'
    __table_args__ = {'schema': 'topology'}
    
    topology_id = Column(INTEGER, primary_key=True, autoincrement=False)
    layer_id = Column(INTEGER, primary_key=True, autoincrement=False)
    schema_name = Column(VARCHAR, nullable=False, autoincrement=False)
    table_name = Column(VARCHAR, nullable=False, autoincrement=False)
    feature_column = Column(VARCHAR, nullable=False, autoincrement=False)
    feature_type = Column(INTEGER, nullable=False, autoincrement=False)
    level = Column(INTEGER, nullable=False, autoincrement=False)
    child_id = Column(INTEGER, autoincrement=False)
