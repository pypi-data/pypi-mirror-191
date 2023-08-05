from sqlalchemy import Column, String, Integer, Date, Float, Boolean, Sequence
from sqlalchemy.ext.declarative import declarative_base

class InpWaterMainAm(declarative_base()):
    __tablename__ = 'inp_water_main_am'
    
    id = Column(Integer, Sequence('seq_inp_water_main_am'), primary_key=True)
    city = Column(String)
    name = Column(String)
    is_ineligib = Column(String)
    is_cond_est = Column(String)
    source = Column(String)
    comments = Column(String)
    project_id = Column(Integer)
    watershed_name = Column(String)
    owner = Column(String)
    ins_date = Column(String)
    dim1 = Column(String)
    dim2 = Column(String)
    stru_type = Column(String)
    material = Column(String)
    inv_file = Column(String)
    rim_ele = Column(String)
    dep_cover = Column(String)
    jnt_type = Column(String)
    ass_us_str = Column(String)
    ass_ds_str = Column(String)
    lat_con = Column(String)
    bed_cond = Column(String)
    trench_bf = Column(String)
    des_life = Column(String)
    des_storm = Column(String)
    function = Column(String)
    thickness = Column(String)
    coating = Column(String)
    lining = Column(String)
    status = Column(String)
    line_cond = Column(String)
    ext_coat_cond = Column(String)
    ht_bedding = Column(String)
    des_str_stru = Column(String)
    str_ins_date = Column(String)
    ext_coat_age = Column(String)
    struc_vint = Column(String)
    struc_class = Column(String)
    us_st_cond = Column(String)
    ds_st_cond = Column(String)
    dis_mater = Column(String)
    soil_type = Column(String)
    gw_table = Column(String)
    location = Column(String)
    dead_load = Column(String)
    live_load = Column(String)
    av_preci_int = Column(String)
    av_preci_dur = Column(String)
    frost_pen = Column(String)
    s_corro = Column(String)
    near_trees = Column(String)
    pipe_dir = Column(String)
    ext_temp = Column(String)
    his_ext_eve = Column(String)
    catch_area = Column(String)
    ws_int = Column(String)
    wet_dry_cyc = Column(String)
    nn_homo_soil = Column(String)
    aci_runoff = Column(String)
    soil_res = Column(String)
    soil_dis = Column(String)
    soil_sul = Column(String)
    soil_ph = Column(String)
    soil_moi_ret = Column(String)
    st_curr = Column(String)
    tidal_inf = Column(String)
    av_flow_vel = Column(String)
    min_flow_vel = Column(String)
    max_flow_vel = Column(String)
    of_freq = Column(String)
    surcharge = Column(String)
    inflow_infill = Column(String)
    exfiltration = Column(String)
    ave_pres = Column(String)
    min_pres = Column(String)
    max_pres = Column(String)
    known_leak = Column(String)
    deb_level = Column(String)
    sed_level = Column(String)
    smell_level = Column(String)
    stag_water = Column(String)
    flooding = Column(String)
    maint_fre = Column(String)
    outelet_prot = Column(String)
    conv_cap = Column(String)
    mode_res_av = Column(String)
    res_2yr = Column(String)
    res_5yr = Column(String)
    res_10yr = Column(String)
    res_25yr = Column(String)
    res_50yr = Column(String)
    res_100yr = Column(String)
    res_500yr = Column(String)
    lt_sim_res = Column(String)
    pacp_cond = Column(String)
    mt_rec = Column(String)
    cctv_rec = Column(String)
    ren_rec = Column(String)
    fail_rec = Column(String)
    comp_rec = Column(String)
    cap_cost = Column(String)
    yr_om_cost = Column(String)
    con_spec = Column(String)
    lof = Column(String)
    eco_imp = Column(String)
    trans_imp = Column(String)
    crit_imp = Column(String)
    utility_imp = Column(String)
    tmdl_imp = Column(String)
    under_pave = Column(String)
    proxi_rail = Column(String)
    repl_cost = Column(String)
    cof = Column(String)
    bre = Column(String)
    cip_id = Column(String)
    max_allow_vel = Column(String)
    max_allow_pres = Column(String)
    mt_score = Column(String)
    vs_inspect_rec = Column(String)
    vs_inspect_score = Column(String)
    em_inspect_rec = Column(String)
    em_inspect_score = Column(String)
    cctv_score = Column(String)
    ac_inspect_rec = Column(String)
    ac_inspect_score = Column(String)
    ultra_test_rec = Column(String)
    ultra_test_score = Column(String)
    pipe_map_rec = Column(String)
    pipe_map_score = Column(String)
    radio_test_rec = Column(String)
    radio_test_score = Column(String)
    thermo_test_rec = Column(String)
    thermo_test_score = Column(String)
    other_test_rec = Column(String)
    other_test_score = Column(String)
    ren_score = Column(String)
    fail_score = Column(String)
    comp_score = Column(String)
    rem_use_life = Column(String)
    watershed_id = Column(String)
    huc_12_id = Column(String)
    land_use = Column(String)
    tree_canopy = Column(String)
    last_inspection_date = Column(String)
    construction_performance_index = Column(String)
    mukey = Column(String)
    cond_comments = Column(String)
    neerstndstr = Column(String)
    pred_flow_area = Column(String)
    is_pred_flow_area = Column(String)
    pred_material = Column(String)
    is_pred_material = Column(String)
    pred_dim1 = Column(String)
    is_pred_dim1 = Column(String)
    pred_dim2 = Column(String)
    is_pred_dim2 = Column(String)
    pred_rimelev = Column(String)
    is_pred_rimelev = Column(String)
    pred_invelev = Column(String)
    is_pred_invelev = Column(String)
    pred_ins_date = Column(String)
    is_pred_ins_date = Column(String)
    enviro_imp = Column(Integer)
    lu_imp = Column(Integer)
    rehab = Column(Boolean)
    rehab_date = Column(Date)
    rehab_material = Column(String)
    condition_date = Column(Date)
    state = Column(String)
    account_id = Column(String)
    rehab_action = Column(String)
    frost_depth = Column(Float)
    gr_water_lvl_frm_land_surf = Column(Float)
    county = Column(String)
    country = Column(String)
    gr_water_station_url = Column(String)
    asset_name = Column(String)
    capacity = Column(Float)

    def __init__(
        self,
        city,
        name,
        is_ineligib,
        is_cond_est,
        source,
        comments,
        project_id,
        watershed_name,
        owner,
        ins_date,
        dim1,
        dim2,
        stru_type,
        material,
        inv_file,
        rim_ele,
        dep_cover,
        jnt_type,
        ass_us_str,
        ass_ds_str,
        lat_con,
        bed_cond,
        trench_bf,
        des_life,
        des_storm,
        function,
        thickness,
        coating,
        lining,
        status,
        line_cond,
        ext_coat_cond,
        ht_bedding,
        des_str_stru,
        str_ins_date,
        ext_coat_age,
        struc_vint,
        struc_class,
        us_st_cond,
        ds_st_cond,
        dis_mater,
        soil_type,
        gw_table,
        location,
        dead_load,
        live_load,
        av_preci_int,
        av_preci_dur,
        frost_pen,
        s_corro,
        near_trees,
        pipe_dir,
        ext_temp,
        his_ext_eve,
        catch_area,
        ws_int,
        wet_dry_cyc,
        nn_homo_soil,
        aci_runoff,
        soil_res,
        soil_dis,
        soil_sul,
        soil_ph,
        soil_moi_ret,
        st_curr,
        tidal_inf,
        av_flow_vel,
        min_flow_vel,
        max_flow_vel,
        of_freq,
        surcharge,
        inflow_infill,
        exfiltration,
        ave_pres,
        min_pres,
        max_pres,
        known_leak,
        deb_level,
        sed_level,
        smell_level,
        stag_water,
        flooding,
        maint_fre,
        outelet_prot,
        conv_cap,
        mode_res_av,
        res_2yr,
        res_5yr,
        res_10yr,
        res_25yr,
        res_50yr,
        res_100yr,
        res_500yr,
        lt_sim_res,
        pacp_cond,
        mt_rec,
        cctv_rec,
        ren_rec,
        fail_rec,
        comp_rec,
        cap_cost,
        yr_om_cost,
        con_spec,
        lof,
        eco_imp,
        trans_imp,
        crit_imp,
        utility_imp,
        tmdl_imp,
        under_pave,
        proxi_rail,
        repl_cost,
        cof,
        bre,
        cip_id,
        max_allow_vel,
        max_allow_pres,
        mt_score,
        vs_inspect_rec,
        vs_inspect_score,
        em_inspect_rec,
        em_inspect_score,
        cctv_score,
        ac_inspect_rec,
        ac_inspect_score,
        ultra_test_rec,
        ultra_test_score,
        pipe_map_rec,
        pipe_map_score,
        radio_test_rec,
        radio_test_score,
        thermo_test_rec,
        thermo_test_score,
        other_test_rec,
        other_test_score,
        ren_score,
        fail_score,
        comp_score,
        rem_use_life,
        watershed_id,
        huc_12_id,
        land_use,
        tree_canopy,
        last_inspection_date,
        construction_performance_index,
        mukey,
        cond_comments,
        neerstndstr,
        pred_flow_area,
        is_pred_flow_area,
        pred_material,
        is_pred_material,
        pred_dim1,
        is_pred_dim1,
        pred_dim2,
        is_pred_dim2,
        pred_rimelev,
        is_pred_rimelev,
        pred_invelev,
        is_pred_invelev,
        pred_ins_date,
        is_pred_ins_date,
        enviro_imp,
        lu_imp,
        rehab,
        rehab_date,
        rehab_material,
        condition_date,
        state,
        account_id,
        rehab_action,
        frost_depth,
        gr_water_lvl_frm_land_surf,
        county,
        country,
        gr_water_station_url,
        asset_name,
        capacity
    ):
        self.city = city
        self.name = name
        self.is_ineligib = is_ineligib
        self.is_cond_est = is_cond_est
        self.source = source
        self.comments = comments
        self.project_id = project_id
        self.watershed_name = watershed_name
        self.owner = owner
        self.ins_date = ins_date
        self.dim1 = dim1
        self.dim2 = dim2
        self.stru_type = stru_type
        self.material = material
        self.inv_file = inv_file
        self.rim_ele = rim_ele
        self.dep_cover = dep_cover
        self.jnt_type = jnt_type
        self.ass_us_str = ass_us_str
        self.ass_ds_str = ass_ds_str
        self.lat_con = lat_con
        self.bed_cond = bed_cond
        self.trench_bf = trench_bf
        self.des_life = des_life
        self.des_storm = des_storm
        self.function = function
        self.thickness = thickness
        self.coating = coating
        self.lining = lining
        self.status = status
        self.line_cond = line_cond
        self.ext_coat_cond = ext_coat_cond
        self.ht_bedding = ht_bedding
        self.des_str_stru = des_str_stru
        self.str_ins_date = str_ins_date
        self.ext_coat_age = ext_coat_age
        self.struc_vint = struc_vint
        self.struc_class = struc_class
        self.us_st_cond = us_st_cond
        self.ds_st_cond = ds_st_cond
        self.dis_mater = dis_mater
        self.soil_type = soil_type
        self.gw_table = gw_table
        self.location = location
        self.dead_load = dead_load
        self.live_load = live_load
        self.av_preci_int = av_preci_int
        self.av_preci_dur = av_preci_dur
        self.frost_pen = frost_pen
        self.s_corro = s_corro
        self.near_trees = near_trees
        self.pipe_dir = pipe_dir
        self.ext_temp = ext_temp
        self.his_ext_eve = his_ext_eve
        self.catch_area = catch_area
        self.ws_int = ws_int
        self.wet_dry_cyc = wet_dry_cyc
        self.nn_homo_soil = nn_homo_soil
        self.aci_runoff = aci_runoff
        self.soil_res = soil_res
        self.soil_dis = soil_dis
        self.soil_sul = soil_sul
        self.soil_ph = soil_ph
        self.soil_moi_ret = soil_moi_ret
        self.st_curr = st_curr
        self.tidal_inf = tidal_inf
        self.av_flow_vel = av_flow_vel
        self.min_flow_vel = min_flow_vel
        self.max_flow_vel = max_flow_vel
        self.of_freq = of_freq
        self.surcharge = surcharge
        self.inflow_infill = inflow_infill
        self.exfiltration = exfiltration
        self.ave_pres = ave_pres
        self.min_pres = min_pres
        self.max_pres = max_pres
        self.known_leak = known_leak
        self.deb_level = deb_level
        self.sed_level = sed_level
        self.smell_level = smell_level
        self.stag_water = stag_water
        self.flooding = flooding
        self.maint_fre = maint_fre
        self.outelet_prot = outelet_prot
        self.conv_cap = conv_cap
        self.mode_res_av = mode_res_av
        self.res_2yr = res_2yr
        self.res_5yr = res_5yr
        self.res_10yr = res_10yr
        self.res_25yr = res_25yr
        self.res_50yr = res_50yr
        self.res_100yr = res_100yr
        self.res_500yr = res_500yr
        self.lt_sim_res = lt_sim_res
        self.pacp_cond = pacp_cond
        self.mt_rec = mt_rec
        self.cctv_rec = cctv_rec
        self.ren_rec = ren_rec
        self.fail_rec = fail_rec
        self.comp_rec = comp_rec
        self.cap_cost = cap_cost
        self.yr_om_cost = yr_om_cost
        self.con_spec = con_spec
        self.lof = lof
        self.eco_imp = eco_imp
        self.trans_imp = trans_imp
        self.crit_imp = crit_imp
        self.utility_imp = utility_imp
        self.tmdl_imp = tmdl_imp
        self.under_pave = under_pave
        self.proxi_rail = proxi_rail
        self.repl_cost = repl_cost
        self.cof = cof
        self.bre = bre
        self.cip_id = cip_id
        self.max_allow_vel = max_allow_vel
        self.max_allow_pres = max_allow_pres
        self.mt_score = mt_score
        self.vs_inspect_rec = vs_inspect_rec
        self.vs_inspect_score = vs_inspect_score
        self.em_inspect_rec = em_inspect_rec
        self.em_inspect_score = em_inspect_score
        self.cctv_score = cctv_score
        self.ac_inspect_rec = ac_inspect_rec
        self.ac_inspect_score = ac_inspect_score
        self.ultra_test_rec = ultra_test_rec
        self.ultra_test_score = ultra_test_score
        self.pipe_map_rec = pipe_map_rec
        self.pipe_map_score = pipe_map_score
        self.radio_test_rec = radio_test_rec
        self.radio_test_score = radio_test_score
        self.thermo_test_rec = thermo_test_rec
        self.thermo_test_score = thermo_test_score
        self.other_test_rec = other_test_rec
        self.other_test_score = other_test_score
        self.ren_score = ren_score
        self.fail_score = fail_score
        self.comp_score = comp_score
        self.rem_use_life = rem_use_life
        self.watershed_id = watershed_id
        self.huc_12_id = huc_12_id
        self.land_use = land_use
        self.tree_canopy = tree_canopy
        self.last_inspection_date = last_inspection_date
        self.construction_performance_index = construction_performance_index
        self.mukey = mukey
        self.cond_comments = cond_comments
        self.neerstndstr = neerstndstr
        self.pred_flow_area = pred_flow_area
        self.is_pred_flow_area = is_pred_flow_area
        self.pred_material = pred_material
        self.is_pred_material = is_pred_material
        self.pred_dim1 = pred_dim1
        self.is_pred_dim1 = is_pred_dim1
        self.pred_dim2 = pred_dim2
        self.is_pred_dim2 = is_pred_dim2
        self.pred_rimelev = pred_rimelev
        self.is_pred_rimelev = is_pred_rimelev
        self.pred_invelev = pred_invelev
        self.is_pred_invelev = is_pred_invelev
        self.pred_ins_date = pred_ins_date
        self.is_pred_ins_date = is_pred_ins_date
        self.enviro_imp = enviro_imp
        self.lu_imp = lu_imp
        self.rehab = rehab
        self.rehab_date = rehab_date
        self.rehab_material = rehab_material
        self.condition_date = condition_date
        self.state = state
        self.account_id = account_id
        self.rehab_action = rehab_action
        self.frost_depth = frost_depth
        self.gr_water_lvl_frm_land_surf = gr_water_lvl_frm_land_surf
        self.county = county
        self.country = country
        self.gr_water_station_url = gr_water_station_url
        self.asset_name = asset_name
        self.capacity = capacity