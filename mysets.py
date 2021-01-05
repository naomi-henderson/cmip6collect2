ms = {}
ms['core_mips']  = ['CMIP', 'ScenarioMIP', 'DAMIP']

ms['fx_tables']    = ['AERfx', 'Efx', 'IfxAnt', 'IfxGre', 'Ofx', 'fx']
ms['yr_tables']    = ['Eyr', 'IyrAnt', 'IyrGre', 'Oyr']
ms['other_tables'] = ['Odec', 'E1hrClimMon','Oclim'] 
ms['mon_tables']   = ['AERmon', 'Amon', 'CFmon', 'Emon', 'ImonAnt', 'ImonGre', 'LImon', 'Lmon', 'Omon', 'SImon']
ms['monZ_tables']  = ['AERmonZ', 'EmonZ']

ms['core_experiments'] = [ '1pctCO2', 'abrupt-4xCO2',  'historical', 'piControl' 
    ,'ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp434', 'ssp460', 'ssp534-over', 'ssp585' ]

ms['more_experiments'] = [ 'piControl-spinup', 'amip-hist', 'esm-hist', 'esm-piControl',
'esm-piControl-spinup' ,'1pctCO2-bgc','lgm', 'past1000', 'amip' ]
                   
ms['core_Amon_2dvars']  = ['clt', 'evspsbl', 'hfls', 'pr', 'prc', 'ps',
                    'psl', 'sfcWind', 'tas', 'ts', 'uas',
                    'vas','huss','hurs']
ms['flux_Amon_2dvars']  = ['rlds', 'rlus', 'rlut', 'rsds', 'rsdt', 'rsus',
                    'rsut', 'rtmt', 'hfds', 'hfls', 'hfss', 'tauu', 'tauv']
ms['core_Amon_3dvars']  = ['ta', 'ua', 'va', 'zg', 'wap', 'hur', 'hus']
ms['extreme_Amon_vars'] = ['tasmax', 'tasmin']
ms['core_Amon_global']  = ['cfc11global', 'cfc12global', 'cfc113global',
                    'ch4global', 'hcfc22global', 'n2oglobal']
ms['other_Amon_vars']   = ['pfull', 'phalf', 'cl', 'co2', 'n2o', 'o3']

ms['core_Omon_2dvars']  = ['tos', 'sos', 'zos']
ms['flux_Omon_2dvars']  = ['tauuo', 'tauvo']
ms['core_Omon_3dvars']  = ['masscello', 'so', 'thetao', 'umo', 'uo', 'vmo',
                    'vo', 'wmo', 'wo']
ms['core_Omon_tracers'] = ['cfc11', 'chl', 'chlos', 'dfe', 'dfeos',
                     'dissic', 'epc100', 'fgco2', 'intpp', 'no3',
                     'no3os', 'o2', 'phyc', 'phycos',
                     'phydiat', 'phydiatos', 'po4', 'sf6', 'si',
                     'sios', 'spco2', 'talk', 'zooc', 'zoocos']
ms['core_Omon_global']  = ['bigthetaoga', 'soga', 'sosga', 'thetaoga',
                    'tosga', 'zostoga']

ms['core_day_2dvars']    = ['clt','hurs', 'huss', 'pr', 'prc', 'ps', 'psl',
                   'rlds', 'rsds', 'sfcWind', 'tas', 'uas', 'vas']
ms['core_day_3dvars']    = ['hur', 'hus', 'ta', 'ua', 'va', 'wap', 'zg']
ms['extreme_day_2dvars'] = ['hursmax', 'hursmin', 'sfcWindmax', 'tasmax', 'tasmin']
ms['flux_day_2dvars']    = ['hfls', 'hfss', 'prsn', 'rlus', 'rlut', 'rsus', 'snw']
ms['land_day_2dvars']    = ['mrro', 'mrso', 'mrsos']

ms['core_3hr_2dvars'] = ['tas', 'ps', 'huss', 'rsds', 'rsdsdiff', 'rsus', 
                         'rlus', 'rlds', 'uas', 'vas']

# define some common searches:
all_search = {}

all_search['A2d-1c'] = {'table_id': ['Amon'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['core_Amon_2dvars']}
all_search['A2d-1f'] = {'table_id': ['Amon'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['flux_Amon_2dvars']}
all_search['A2d-1e'] = {'table_id': ['Amon'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['extreme_Amon_vars']}
all_search['A3d-1c'] = {'table_id': ['Amon'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['core_Amon_3dvars']}

all_search['O2d-1f'] = {'table_id': ['Omon'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['flux_Omon_2dvars']}
all_search['O2d-1c'] = {'table_id': ['Omon'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['core_Omon_2dvars']}
all_search['O3d-1c'] = {'table_id': ['Omon'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['core_Omon_3dvars']}
all_search['O3d-1t'] = {'table_id': ['Omon'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['core_Omon_tracers']}
all_search['Omon-1g'] = {'table_id': ['Omon'], 'experiment_id':
                         ms['core_experiments'], 'variable_id':
                         ms['core_Omon_global']}

all_search['D2d-1c'] = {'table_id': ['day'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['core_day_2dvars']}
all_search['D2d-1e'] = {'table_id': ['day'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['extreme_day_2dvars']}
all_search['D2d-1f'] = {'table_id': ['day'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['flux_day_2dvars']}
all_search['D2d-1l'] = {'table_id': ['day'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['land_day_2dvars']}
all_search['D3d-1c'] = {'table_id': ['day'], 'experiment_id':
                        ms['core_experiments'], 'variable_id':
                        ms['core_day_3dvars']}

all_search['other-coremips'] = {'table_id': ms['other_tables'],
                                'activity_id': ms['core_mips']}
all_search['fx-coremips'] = {'table_id': ms['fx_tables'],
                                'activity_id': ms['core_mips']}
all_search['yr-coremips'] = {'table_id': ms['yr_tables'],
                             'activity_id': ms['core_mips']}

all_search['3hr-historical'] = {'table_id': ['3hr'],
                             'experiment_id': ['historical'],
                             'variable_id': ms['core_3hr_2dvars']}
all_search['3hr-ssp1'] = {'table_id': ['3hr'],
                             'experiment_id': ['ssp245', 'ssp370'],
                             'variable_id': ms['core_3hr_2dvars']}
all_search['3hr-ssp2'] = {'table_id': ['3hr'],
                             'experiment_id': ['esm-hist', 'ssp126', 'ssp585'],
                             'variable_id': ms['core_3hr_2dvars']}
all_search['3hr-hist1'] = {'table_id': ['3hr'],
                             'experiment_id': ['historical'],
                             'variable_id': ['tas', 'uas', 'vas']}
all_search['3hr-hist2'] = {'table_id': ['3hr'],
                             'experiment_id': ['historical'],
                             'variable_id': ['ps', 'huss', 'rsds', 'rsdsdiff', 'rsus','rlus', 'rlds']}

