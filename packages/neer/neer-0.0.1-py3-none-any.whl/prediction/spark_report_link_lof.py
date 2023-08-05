from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

class SparkReportLinkLof(declarative_base()):
    __tablename__ = 'spark_report_link_lof'
    __table_args__ = {"schema": "predictions"}

    project_id = Column(Integer, primary_key=True)
    simulation_id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    flow_area = Column(Float)
    pred_material = Column(Boolean)
    pred_dsinvelev = Column(Boolean)
    pred_usinvelev = Column(Boolean)
    material = Column(String)
    ds_inv_elev = Column(Float)
    us_inv_elev = Column(Float)
    lof = Column(Float)
    created_at = Column(DateTime(timezone=True), nullable=True, primary_key=True)
    updated_at = Column(DateTime(timezone=True))

    def __init__(
        self,
        project_id,
        simulation_id,
        name,
        flow_area,
        pred_material,
        pred_dsinvelev,
        pred_usinvelev,
        material,
        ds_inv_elev,
        us_inv_elev,
        lof,
        created_at,
        updated_at
    ):
        self.project_id = project_id
        self.simulation_id = simulation_id
        self.name = name
        self.flow_area = flow_area
        self.pred_material = pred_material
        self.pred_dsinvelev = pred_dsinvelev
        self.pred_usinvelev = pred_usinvelev
        self.material = material
        self.ds_inv_elev = ds_inv_elev
        self.us_inv_elev = us_inv_elev
        self.lof = lof
        self.created_at = created_at,
        self.updated_at = updated_at