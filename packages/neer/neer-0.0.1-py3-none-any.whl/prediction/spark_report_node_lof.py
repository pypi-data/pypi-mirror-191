from sqlalchemy import Column, String, Integer, DateTime, Date, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

class SparkReportNodeLof(declarative_base()):
    __tablename__ = 'spark_report_node_lof'
    __table_args__ = {"schema": "predictions"}

    project_id = Column(Integer, primary_key=True)
    simulation_id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    flow_area = Column(Float)
    ins_date = Column(Date)
    pred_material = Column(Boolean)
    pred_dim1 = Column(Boolean)
    pred_dim2 = Column(Boolean)
    pred_rimelev = Column(Boolean)
    pred_invelev = Column(Boolean)
    material = Column(String)
    dim1 = Column(Float)
    dim2 = Column(Float)
    rim_ele = Column(Float)
    inv_ele = Column(Float)
    lof = Column(Float)
    created_at = Column(DateTime(timezone=True), nullable=True, primary_key=True)
    updated_at = Column(DateTime(timezone=True))

    def __init__(
        self,
        project_id,
        simulation_id,
        name,
        flow_area,
        ins_date,
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
        self.ins_date = ins_date
        self.pred_material = pred_material
        self.pred_dsinvelev = pred_dsinvelev
        self.pred_usinvelev = pred_usinvelev
        self.material = material
        self.ds_inv_elev = ds_inv_elev
        self.us_inv_elev = us_inv_elev
        self.lof = lof
        self.created_at = created_at,
        self.updated_at = updated_at