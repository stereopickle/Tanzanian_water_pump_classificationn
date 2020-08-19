#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:55:17 2020

@author: Eunjoo Byeon

This file contains the preprocessing pipeline.

"""


import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import dictionaries as di


def preprocessing(X0):
    X = X0.copy()
    # fill missing values
    X['funder'] = X.funder.fillna('Unknown')
    X['installer'] = X.installer.fillna('Unknown')
    X['scheme_management'] = X.scheme_management.fillna('Unknown')
    X['scheme_name'] = X.scheme_name.fillna('None')
    
    freq_subvil = di.freq_subvil
    
    X['temp_subvil'] = [freq_subvil[x] for x in X['region']]
    X['subvillage'] = np.where(X['subvillage'].isnull(), X['temp_subvil'], X['subvillage'])

    X['public_meeting'] = X.public_meeting.fillna(True)

    X['permit']= X.permit.mask(X.permit.isnull(), 
      np.random.choice([True, False], size=len(X)))
    
    X['permit'] = X.permit.astype('bool')
    
    avg_lat_long = pd.read_pickle('PKL/avg_lat_long.pkl')
    
    X['latitude'] = np.where(X.longitude < 5, 
         avg_lat_long['latitude'][X.region], X.latitude)
    X['longitude'] = np.where(X.longitude < 5, 
             avg_lat_long['longitude'][X.region], X.longitude)
        
    # change date to year
    X['date_recorded'] = [int(x[:4]) for x in X.date_recorded]
    
    # change data types
    X['region_code'] = X['region_code'].astype('object')
    X['district_code'] = X['district_code'].astype('object')
    
    # fixing texts
    text_feats = di.text_feats
    for c in text_feats:
        X[c] = [x.lower() for x in X[c]]

    # funders 
    cond = [X.funder.str.contains('mganga'), 
        X.funder.str.contains('mwin'), 
        X.funder.isin(['mwanza', 'mwanga town water authority']),
        (X.funder.isin(di.roman_catholic)) | X.funder.str.contains('roma'), 
        X.funder.isin(di.unicef), 
        X.funder.isin(di.netherland), 
        (X.funder.str.contains('kkkt')) | (X.funder.str.contains('elc')) | (X.funder.isin(di.lutheran)), 
        X.funder.str.contains('danid'), 
        X.funder.str.contains('hes'),
        X.funder.isin(di.world_bank) | (X.funder.str.contains('world') & X.funder.str.contains('bank')),
        (X.funder.isin(di.world_vision)) | (X.funder.str.contains('world') & X.funder.str.contains('vision')),
        (X.funder.str.contains('tasa') | (X.funder.str.contains('tass'))),
        X.funder.str.contains('germa'), 
        X.funder.str.contains('distri'), 
        (X.funder.str.contains('dhv')) | (X.funder == 'dh') , 
        X.funder.isin(di.private_individual), 
        X.funder.str.contains('dws'), 
        X.funder.str.contains('nora'), 
        X.funder.str.contains('tcrs'), 
        X.funder.str.contains('heal'), 
        X.funder.str.contains('dwe'), 
        X.funder.isin(di.ADB), 
        (X.funder.str.contains('lga')) | (X.funder.str.contains('loca')),
        X.funder.str.contains('amre'), 
        X.funder.str.contains('oxf'), 
        (X.funder.str.contains('fin')) & (X.funder.str.contains('w')), 
        (X.funder.str.contains('jap')) | (X.funder.isin(['jica', 'jaica'])),
        X.funder.str.contains('isf') | (X.funder == 'is'),
        (X.funder.str.contains('chri')) | (X.funder.str.contains('cris')),
        X.funder.str.contains('das'),
        X.funder.str.contains('taca'), 
        X.funder.str.contains('compas'),
        X.funder.str.contains('vil'),
        X.funder.str.contains('conce'),
        X.funder.str.contains('egy'),
        X.funder.str.contains('meth'), 
        X.funder.str.contains('edk'),
        X.funder.str.contains('finl'),
        X.funder.str.contains('irev'),
        X.funder.isin(di.baptist),
        (X.funder.str.contains('chur'))| X.funder.str.contains('miss'),
        X.funder.isin(di.unknown),
        X.funder.str.contains('schoo'),
        (X.funder.str.contains('rws')) | (X.funder.str.contains('rural') & X.funder.str.contains('wat')),
        X.funder.str.contains('ded'),
        X.funder.str.contains('oik'),
        (X.funder.str.contains('kil') & X.funder.str.contains('wat')), 
        X.funder.str.contains('comm'), 
        X.funder.str.contains('farm'),
        X.funder.str.contains('apm'),
        X.funder.str.contains('africar'), 
        X.funder.isin(di.swedish),
        X.funder.str.contains('wfp'), 
        (X.funder.str.contains('wat') & X.funder.str.contains('aid')), 
        X.funder.str.contains('drdp'), 
        (X.funder.str.contains('wat') & X.funder.str.contains('use')), 
        X.funder.str.contains('muni')
       ]
    vals = ['mganga', 'mwinjuma_mzee', 'mwanza', 'roman_catholic', 'unicef', 
            'netherland', 'kkkt', 'danida', 'hesawa', 'world_bank', 
            'world_vision', 'tasaf', 'germany', 'district council', 'dhv', 
            'individual', 'dwsp', 'norad', 'tcrs','ministry_of_health', 'dwe', 
            'adb', 'lga', 'amref', 'oxfam', 'finwater', 'japan', 'isf', 
            'christian','dasp', 'tacare', 'compassion', 'village', 'concern',
            'egype', 'methodist', 'friedkin', 'finland','irevea', 'baptist',
            'other_church', 'unknown', 'school','rwssp', 'ded', 'oikos', 
            'killi_water', 'community', 'farm_afr', 'apm', 'africare','sweden', 
            'wfp', 'wateraid', 'drdp', 'wateruser', 'municipal_council']
    
    X.funder = np.select(cond, vals, X.funder)
    
    # installers


    for k, v in di.typos.items():
        X.installer = X.installer.apply(lambda x: x.replace(k, v))
    for k, v in di.str_isin.items():
        X.installer = np.where(X.installer.isin(v), k, X.installer)
    for k, v in di.str_startswith.items():
        X.installer = np.where(X.installer.str.startswith(k), v, X.installer)
    for k, v in di.str_contains.items():
        X.installer = np.where(X.installer.str.contains(k), v, X.installer)
    for k, v in di.str_endswith.items():
        X.installer = np.where(X.installer.str.endswith(k), v, X.installer)
        


    # limiting to values with at least 100 observations
    other_funders = [x for x in set(X.funder) if len(X[X.funder == x]) < 50]
    X['funder'] = np.where(X.funder.isin(other_funders), 'others', X.funder)
    
    other_installer = [x for x in set(X.installer) if len(X[X.installer == x]) < 100]
    X['installer'] = np.where(X.installer.isin(other_installer), 'others', X.installer)

    # Feature engineering
    X['negative_gps_height'] = np.where(X.gps_height < 0, 1, 0)
    X['zero_gps_height'] = np.where(X.gps_height == 0, 1, 0)
    
    cond = [X.construction_year > 2005, 
       X.construction_year > 2000, 
       X.construction_year > 1990, 
       X.construction_year > 1980, 
       X.construction_year > 1970]
    vals = ['after05', '00s', '90s', '80s', '70s']

    X['built_recent'] = np.select(cond, vals, 'others')
    
    # new column: n_wells_village
    subvil_counts = X.subvillage.value_counts()
    cond = [subvil_counts[X.subvillage] > 300, 
            subvil_counts[X.subvillage] > 100,
            subvil_counts[X.subvillage] > 50, subvil_counts[X.subvillage] > 10]
    vals = ['more_than_300', 'more_than_100', 'more_than50', 'more_than_10']
    X['n_wells_village'] = np.select(cond, vals, 'less_than_10')
    
    # turn less than 100 wells village into 'others'
    other_subvill =  [x for x in set(X.subvillage) if len(X[X.subvillage == x]) < 100]
    X['subvillage'] = np.where(X.subvillage.isin(other_subvill), 'others', X.subvillage)
    
    def get_lat_long(location):
        ''' helper: return a tuple of long, lat '''
        geolocator = Nominatim(user_agent = "Tanzwater")
        location = geolocator.geocode(location)
        return (location.longitude, location.latitude)
    
    def run_get_lat_long(bas):
        ''' return a tuple of long, lat '''
        try:
            return get_lat_long(bas)
        except AttributeError:
            bas_new = bas.title()
            try: 
                return get_lat_long(bas_new)
            except: 
                return (0,0)
    
    # basin long lat     

    allbasins = di.allbasins
    basins = set(X.basin)
    
    for basin in basins:
        if basin not in allbasins.keys():
            allbasins[basin] = run_get_lat_long(basin)
    
    X['basin_lat'] = X.basin.apply(lambda x: allbasins[x][1])
    X['basin_long'] = X.basin.apply(lambda x: allbasins[x][0])
    
    # distance to basin 
    
    def get_dist(crd1, crd2): 
        return geodesic(crd1, crd2).miles

    X['dist_to_basin'] = X.apply(lambda x: get_dist((x.latitude, x.longitude), 
                                (x.basin_lat, x.basin_long)), axis = 1)   
    
    # if failed to find basin location, make it 0.
    X['dist_to_basin'] = np.where((X.basin_lat == 0) & (X.basin_long == 0), 
             0, X.dist_to_basin)
    
    # LGA
    # fix typo
    X.lga = X.lga.replace({'missungwi': 'misungwi', 'misenyi':'missenyi'})
    alllgas = di.alllgas
    
    lgas = set(X.lga)
    
    for lg in lgas:
        if lg not in alllgas.keys():
            alllgas[lg] = run_get_lat_long(lg)
            
    X['lga_lat'] = X.lga.apply(lambda x: alllgas[x][1])
    X['lga_long'] = X.lga.apply(lambda x: alllgas[x][0])
    
    X['dist_to_lga'] = X.apply(lambda x: get_dist((x.latitude, x.longitude), 
                            (x.lga_lat, x.lga_long)), axis = 1)
    
    # if failed to find lga location, make it 0.
    X['dist_to_lga'] = np.where((X.lga_lat == 0) & (X.lga_long == 0), 
             0, X.dist_to_lga)
        
    
    # make sure they are float
    X.lga_lat = X.lga_lat.astype('float')
    X.lga_long = X.lga_long.astype('float')
    X.basin_lat = X.basin_lat.astype('float')
    X.basin_long = X.basin_long.astype('float')
    
    # separate out urban and rural lga
    X['urban_lga'] = X.ward.str.contains('urban')
    X['rural_lga'] = X.ward.str.contains('rural')
    
    # turn less than 100 wells into 'others'
    other_lga =  [x for x in set(X.lga) if len(X[X.lga == x]) < 100]
    X['lga'] = np.where(X.lga.isin(other_lga), 'others', X.lga)    
    
    # separate out urban and rural wards
    X['urban_wards'] = X.ward.str.contains('urban')
    X['rural_wards'] = X.ward.str.contains('rural')   
    
    
    # add the extraction type class
    chosen =  [x for x in set(X.extraction_type) if len(X[X.extraction_type == x]) > 100]
    X['extraction_type_c'] = np.where(X.extraction_type.isin(chosen), X.extraction_type, X.extraction_type_group)
    
    # final columns
    cols = ['amount_tsh', 'date_recorded', 'funder', 'gps_height', 'installer',
       'longitude', 'latitude', 'num_private', 'basin', 'subvillage', 'region',
       'district_code', 'lga', 'population', 'public_meeting',
       'scheme_management', 'permit', 'construction_year', 'management',
       'payment_type', 'water_quality', 'quantity', 'source',
       'waterpoint_type', 'negative_gps_height', 'zero_gps_height',
       'built_recent', 'n_wells_village', 'basin_lat', 'basin_long',
       'dist_to_basin', 'lga_lat', 'lga_long', 'dist_to_lga', 'urban_lga',
       'rural_lga', 'urban_wards', 'rural_wards', 'extraction_type_c']
    
    return X[cols]
    
    
    
    
    
    
    
    