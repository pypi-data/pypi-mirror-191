from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

class MaterialServiceLife(declarative_base()):
    __tablename__ = 'material_service_life'
    
    id = Column(Integer, primary_key=True)
    material = Column(String)
    service_life_years = Column(Integer)
    project_type = Column(String)
    structure_type = Column(String)
    structure_details = Column(String)

    def __init__(
        self,
        material,
        service_life_years,
        project_type,
        structure_type,
        structure_details
    ):
        self.material = material
        self.service_life_years = service_life_years
        self.project_type = project_type
        self.structure_type = structure_type
        self.structure_details = structure_details