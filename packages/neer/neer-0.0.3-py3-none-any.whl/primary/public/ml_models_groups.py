from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, BIT
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class MlModelsGroups(PrimaryBase):
    __tablename__ = 'ml_models_groups'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    team_id = Column(INTEGER, autoincrement=False)
    user_id = Column(INTEGER, autoincrement=False)
    name = Column(TEXT, nullable=False, autoincrement=False)
    description = Column(TEXT, autoincrement=False)
    model_type = Column(TEXT, nullable=False, autoincrement=False)
    model_prediction = Column(TEXT, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    is_generic = Column(BIT, nullable=False, autoincrement=False)
    model_network = Column(TEXT, autoincrement=False)
