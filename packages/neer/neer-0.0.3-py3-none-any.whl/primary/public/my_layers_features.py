from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class MyLayersFeatures(PrimaryBase):
    __tablename__ = 'my_layers_features'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    my_layer_id = Column(INTEGER, nullable=False, autoincrement=False)
    type = Column(VARCHAR(191), nullable=False, autoincrement=False)
    geometry = Column(TEXT, nullable=False, autoincrement=False)
    properties = Column(TEXT, nullable=False, autoincrement=False)
