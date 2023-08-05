from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

class Simulations(declarative_base()):
    __tablename__ = 'simulations'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer)
    user_id = Column(Integer)
    name = Column(String)
    rpt_name = Column(String)
    status = Column(String)
    message = Column(String)
    analysis_begun_on = Column(String)
    analysis_ended_on = Column(String)
    inp_file = Column(String)
    subcatchment_file = Column(String)
    node_file = Column(String)
    link_file = Column(String)
    text_file = Column(String)
    report_file = Column(String)
    out_file = Column(String)
    json_file = Column(String)
    created_at = Column(DateTime(timezone=False))
    updated_at = Column(DateTime(timezone=False))
    reports_parser_status = Column(Integer)
    links_parser_status = Column(Integer)
    nodes_parser_status = Column(Integer)
    subcatchments_parser_status = Column(Integer)
    nodes = Column(Integer)
    links = Column(Integer)
    subcatchments = Column(Integer)
    nodes_inserted = Column(Integer)
    links_inserted = Column(Integer)
    subcatchments_inserted = Column(Integer)
    use_real_time_data = Column(String)
    option_start_date_time = Column(DateTime(timezone=False))
    option_end_date_time = Column(DateTime(timezone=True))
    parsed_node_file = Column(String)
    parsed_link_file = Column(String)
    parsed_subcatchment_file = Column(String)
    is_auto = Column(Integer)
    node_geojson = Column(String)
    link_geojson = Column(String)
    subcatchment_geojson = Column(String)
    group_name = Column(String)
    forecast = Column(String)
    hindcast = Column(String)
    is_backtest = Column(Integer)
    floodplain_boundary_output = Column(String)
    depth_raster_output = Column(String)
    water_surface_elevation_raster_output = Column(String)
    velocity_raster_output = Column(String)
    flood_severity_raster_output = Column(String)
    wms_url_fbo = Column(String)
    wfs_url_fbo = Column(String)
    wms_url_dro = Column(String)
    wfs_url_dro = Column(String)
    wms_url_wser = Column(String)
    wfs_url_wser = Column(String)
    wms_url_vro = Column(String)
    wfs_url_vro = Column(String)
    wms_url_fsro = Column(String)
    wfs_url_fsro = Column(String)
    vro_legend_url = Column(String)
    dro_legend_url = Column(String)
    fsro_legend_url = Column(String)
    wser_legend_url = Column(String)
    lof_nodes_completed = Column(Integer)
    lof_links_completed = Column(Integer)
    flooded_structures_path = Column(String)
    flooded_roads_path = Column(String)
    parsing_begun_on = Column(DateTime(timezone=True))
    parsing_ended_on = Column(DateTime(timezone=True))
    risk_map_status = Column(Integer)
    floodplain_status = Column(Integer)
    geoserver_status = Column(Integer)
    floodplain_intersection_status = Column(Integer)
    rainfall_event_id = Column(Integer)

    def __init__(
        self,
        project_id,
        user_id,
        name,
        rpt_name,
        status,
        message,
        analysis_begun_on,
        analysis_ended_on,
        inp_file,
        subcatchment_file,
        node_file,
        link_file,
        text_file,
        report_file,
        out_file,
        json_file,
        created_at,
        updated_at,
        reports_parser_status,
        links_parser_status,
        nodes_parser_status,
        subcatchments_parser_status,
        nodes,
        links,
        subcatchments,
        nodes_inserted,
        links_inserted,
        subcatchments_inserted,
        use_real_time_data,
        option_start_date_time,
        option_end_date_time,
        parsed_node_file,
        parsed_link_file,
        parsed_subcatchment_file,
        is_auto,
        node_geojson,
        link_geojson,
        subcatchment_geojson,
        group_name,
        forecast,
        hindcast,
        is_backtest,
        floodplain_boundary_output,
        depth_raster_output,
        water_surface_elevation_raster_output,
        velocity_raster_output,
        flood_severity_raster_output,
        wms_url_fbo,
        wfs_url_fbo,
        wms_url_dro,
        wfs_url_dro,
        wms_url_wser,
        wfs_url_wser,
        wms_url_vro,
        wfs_url_vro,
        wms_url_fsro,
        wfs_url_fsro,
        vro_legend_url,
        dro_legend_url,
        fsro_legend_url,
        wser_legend_url,
        lof_nodes_completed,
        lof_links_completed,
        flooded_structures_path,
        flooded_roads_path,
        parsing_begun_on,
        parsing_ended_on,
        risk_map_status,
        floodplain_status,
        geoserver_status,
        floodplain_intersection_status,
        rainfall_event_id
    ):
        self.project_id = project_id
        self.user_id = user_id
        self.name = name
        self.rpt_name = rpt_name
        self.status = status
        self.message = message
        self.analysis_begun_on = analysis_begun_on
        self.analysis_ended_on = analysis_ended_on
        self.inp_file = inp_file
        self.subcatchment_file = subcatchment_file
        self.node_file = node_file
        self.link_file = link_file
        self.text_file = text_file
        self.report_file = report_file
        self.out_file = out_file
        self.json_file = json_file
        self.created_at = created_at
        self.updated_at = updated_at
        self.reports_parser_status = reports_parser_status
        self.links_parser_status = links_parser_status
        self.nodes_parser_status = nodes_parser_status
        self.subcatchments_parser_status = subcatchments_parser_status
        self.nodes = nodes
        self.links = links
        self.subcatchments = subcatchments
        self.nodes_inserted = nodes_inserted
        self.links_inserted = links_inserted
        self.subcatchments_inserted = subcatchments_inserted
        self.use_real_time_data = use_real_time_data
        self.option_start_date_time = option_start_date_time
        self.option_end_date_time = option_end_date_time
        self.parsed_node_file = parsed_node_file
        self.parsed_link_file = parsed_link_file
        self.parsed_subcatchment_file = parsed_subcatchment_file
        self.is_auto = is_auto
        self.node_geojson = node_geojson
        self.link_geojson = link_geojson
        self.subcatchment_geojson = subcatchment_geojson
        self.group_name = group_name
        self.forecast = forecast
        self.hindcast = hindcast
        self.is_backtest = is_backtest
        self.floodplain_boundary_output = floodplain_boundary_output
        self.depth_raster_output = depth_raster_output
        self.water_surface_elevation_raster_output = water_surface_elevation_raster_output
        self.velocity_raster_output = velocity_raster_output
        self.flood_severity_raster_output = flood_severity_raster_output
        self.wms_url_fbo = wms_url_fbo
        self.wfs_url_fbo = wfs_url_fbo
        self.wms_url_dro = wms_url_dro
        self.wfs_url_dro = wfs_url_dro
        self.wms_url_wser = wms_url_wser
        self.wfs_url_wser = wfs_url_wser
        self.wms_url_vro = wms_url_vro
        self.wfs_url_vro = wfs_url_vro
        self.wms_url_fsro = wms_url_fsro
        self.wfs_url_fsro = wfs_url_fsro
        self.vro_legend_url = vro_legend_url
        self.dro_legend_url = dro_legend_url
        self.fsro_legend_url = fsro_legend_url
        self.wser_legend_url = wser_legend_url
        self.lof_nodes_completed = lof_nodes_completed
        self.lof_links_completed = lof_links_completed
        self.flooded_structures_path = flooded_structures_path
        self.flooded_roads_path = flooded_roads_path
        self.parsing_begun_on = parsing_begun_on
        self.parsing_ended_on = parsing_ended_on
        self.risk_map_status = risk_map_status
        self.floodplain_status = floodplain_status
        self.geoserver_status = geoserver_status
        self.floodplain_intersection_status = floodplain_intersection_status
        self.rainfall_event_id = rainfall_event_id