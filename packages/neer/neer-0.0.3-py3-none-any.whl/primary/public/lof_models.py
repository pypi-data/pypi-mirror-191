from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class LofModels(PrimaryBase):
    __tablename__ = 'lof_models'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    s3_model_uri = Column(VARCHAR(191), nullable=False, autoincrement=False)
    s3_scaler_uri = Column(VARCHAR(191), nullable=False, autoincrement=False)
    input_table_name = Column(VARCHAR(191), nullable=False, autoincrement=False)
    input_table_cols = Column(VARCHAR(191), nullable=False, autoincrement=False)
    trained_on = Column(TIMESTAMP, nullable=False, autoincrement=False)
    is_stacked = Column(INTEGER, autoincrement=False)
    is_generic = Column(INTEGER, autoincrement=False)
    team_id = Column(INTEGER, autoincrement=False)
    name = Column(VARCHAR(191), autoincrement=False)
    output_table_name = Column(VARCHAR(191), autoincrement=False)
    output_table_col = Column(VARCHAR(191), autoincrement=False)
    description = Column(VARCHAR(191), autoincrement=False)
    project_type = Column(VARCHAR(50), autoincrement=False)
    parent_model_id = Column(INTEGER, autoincrement=False)
    order = Column(INTEGER, autoincrement=False)
    s3_python_uri = Column(TEXT, autoincrement=False)
    python_update_version = Column(TEXT, autoincrement=False)
    python_update_version  = Column(INTEGER, autoincrement=False)
