from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

class MachineLearningModelsPrediction(declarative_base()):
    __tablename__ = 'ml_models_predictions'

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer)
    value = Column(String)
    predicted_at = Column(Date)
    user_id = Column(Integer)
    object_id = Column(String)
    label = Column(String)

    def __init__(
        self,
        model_id,
        value,
        predicted_at,
        user_id,
        object_id,
        label
    ):
        self.model_id = model_id
        self.value = value
        self.predicted_at = predicted_at
        self.user_id = user_id
        self.object_id = object_id
        self.label = label