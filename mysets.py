core_mips = ['CMIP', 'ScenarioMIP', 'DAMIP']

fx_tables = ['AERfx', 'Efx', 'IfxAnt', 'IfxGre', 'Ofx', 'fx']
yr_tables = ['Eyr', 'IyrAnt', 'IyrGre', 'Oyr']
other_tables = ['Odec', 'E1hrClimMon','Oclim'] 
mon_tables = ['AERmon', 'Amon', 'CFmon', 'Emon', 'ImonAnt', 'ImonGre', 'LImon', 'Lmon', 'Omon', 'SImon']
monZ_tables = ['AERmonZ', 'EmonZ']

core_experiments = [
    '1pctCO2', 'abrupt-4xCO2',  'historical', 'piControl' 
    ,'ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp434', 'ssp460',
'ssp534-over', 'ssp585'
                   ]
more_experiments = [
     'piControl-spinup', 'amip-hist', 'esm-hist', 'esm-piControl',
'esm-piControl-spinup'
    ,'1pctCO2-bgc','lgm', 'past1000', 'amip'
                   ]
                   
core_Amon_2dvars = ['clt', 'evspsbl', 'hfls', 'pr', 'prc', 'ps',
                    'psl', 'sfcWind', 'tas', 'ts', 'uas',
                    'vas','huss','hurs']
flux_Amon_2dvars = ['rlds', 'rlus', 'rlut', 'rsds', 'rsdt', 'rsus',
                    'rsut', 'rtmt', 'hfds', 'hfls', 'hfss', 'tauu',
                    'tauv']
core_Amon_3dvars = ['ta', 'ua', 'va', 'zg', 'wap', 'hur', 'hus']
extreme_Amon_vars = ['tasmax', 'tasmin']
core_Amon_global = ['cfc11global', 'cfc12global', 'cfc113global',
                    'ch4global', 'hcfc22global', 'n2oglobal']
other_Amon_vars = ['pfull', 'phalf', 'cl', 'co2', 'n2o', 'o3']

core_Omon_2dvars = ['tos', 'sos', 'zos']
flux_Omon_2dvars = ['tauuo', 'tauvo']
core_Omon_3dvars = ['masscello', 'so', 'thetao', 'umo', 'uo', 'vmo',
                    'vo', 'wmo', 'wo']
core_Omon_tracers = ['cfc11', 'chl', 'chlos', 'dfe', 'dfeos',
                     'dissic', 'epc100', 'fgco2', 'intpp', 'no3',
                     'no3os', 'o2', 
                                          'phyc', 'phycos',
                     'phydiat', 'phydiatos', 'po4', 'sf6', 'si',
                     'sios', 'spco2', 'talk', 'zooc', 'zoocos']
core_Omon_global = ['bigthetaoga', 'soga', 'sosga', 'thetaoga',
                    'tosga', 'zostoga']

core_day_2dvars = ['clt','hurs', 'huss', 'pr', 'prc', 'ps', 'psl',
                   'rlds', 'rsds', 'sfcWind', 'tas', 'uas', 'vas']
core_day_3dvars = ['hur', 'hus', 'ta', 'ua', 'va', 'wap', 'zg']
extreme_day_2dvars = ['hursmax', 'hursmin', 'sfcWindmax', 'tasmax',
                      'tasmin']
flux_day_2dvars = ['hfls', 'hfss', 'prsn', 'rlus', 'rlut', 'rsus',
                   'snw']
land_day_2dvars = ['mrro', 'mrso', 'mrsos']


# define some common searches:
all_search = {}

all_search['A2d-1c'] = {'table_id': ['Amon'], 'experiment_id': core_experiments, 'variable_id': core_Amon_2dvars}
all_search['A2d-1f'] = {'table_id': ['Amon'], 'experiment_id': core_experiments, 'variable_id': flux_Amon_2dvars}
all_search['A2d-1e'] = {'table_id': ['Amon'], 'experiment_id': core_experiments, 'variable_id': extreme_Amon_vars}
all_search['A3d-1c'] = {'table_id': ['Amon'], 'experiment_id': core_experiments, 'variable_id': core_Amon_3dvars}

all_search['O2d-1f'] = {'table_id': ['Omon'], 'experiment_id': core_experiments, 'variable_id': flux_Omon_2dvars}
all_search['O2d-1c'] = {'table_id': ['Omon'], 'experiment_id': core_experiments, 'variable_id': core_Omon_2dvars}
all_search['O3d-1c'] = {'table_id': ['Omon'], 'experiment_id': core_experiments, 'variable_id': core_Omon_3dvars}
all_search['O3d-1t'] = {'table_id': ['Omon'], 'experiment_id': core_experiments, 'variable_id': core_Omon_tracers}

all_search['other-coremips'] = {'table_id': other_tables, 'activity_id': core_mips}
all_search['fx-coremips'] = {'table_id': fx_tables, 'activity_id': core_mips}
all_search['yr-coremips'] = {'table_id': yr_tables, 'activity_id': core_mips}

