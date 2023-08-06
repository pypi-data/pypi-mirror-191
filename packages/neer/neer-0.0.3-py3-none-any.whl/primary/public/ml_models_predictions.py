from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class MlModelsPredictions(PrimaryBase):
    __tablename__ = 'ml_models_predictions'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    model_id = Column(INTEGER, nullable=False, autoincrement=False)
    value = Column(VARCHAR(191), nullable=False, autoincrement=False)
    predicted_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    user_id = Column(INTEGER, nullable=False, autoincrement=False)
    object_id = Column(VARCHAR(191), autoincrement=False)
    label = Column(VARCHAR(191), autoincrement=False)
