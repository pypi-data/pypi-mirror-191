from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class StructureUnitCostLookup(PrimaryBase):
    __tablename__ = 'structure_unit_cost_lookup'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    esri_oid = Column(INTEGER, nullable=False, autoincrement=False)
    replacement_unit_name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    unit_cost_under_pavement = Column(INTEGER, nullable=False, autoincrement=False)
    unit_cost_not_under_pavement = Column(INTEGER, nullable=False, autoincrement=False)
