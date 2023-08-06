from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class MyLayerFiles(PrimaryBase):
    __tablename__ = 'my_layer_files'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(BIGINT, nullable=False, autoincrement=False)
    name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    path = Column(VARCHAR(191), autoincrement=False)
    columns = Column(TEXT, autoincrement=False)
    geometry_type = Column(VARCHAR(191), autoincrement=False)
