from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from base import PrimaryBase

class TypeormMetadata(PrimaryBase):
    __tablename__ = 'typeorm_metadata'
    __table_args__ = {'schema': 'public'}
    
    column_not_exist_in_db = Column(INTEGER, primary_key=True) # Needed to circumvent primary key requirement in sqlalchemy
    type = Column(VARCHAR, nullable=False, autoincrement=False)
    database = Column(VARCHAR, autoincrement=False)
    schema = Column(VARCHAR, autoincrement=False)
    table = Column(VARCHAR, autoincrement=False)
    name = Column(VARCHAR, autoincrement=False)
    value = Column(TEXT, autoincrement=False)
