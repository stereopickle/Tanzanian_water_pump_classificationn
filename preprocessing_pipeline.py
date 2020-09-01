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
import string
from collections import Counter
import pickle

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
    
    
    avg_lat_long = pd.read_pickle('PKL/avg_lat_long.pkl')
    
    X['latitude'] = np.where(X.longitude < 5,
                             avg_lat_long['latitude'][X.region], X.latitude)
    X['longitude'] = np.where(X.longitude < 5,
                              avg_lat_long['longitude'][X.region], X.longitude)
        
    # change date to year
    X['year_recorded'] = [int(x[:4]) for x in X.date_recorded]
    X['month_recorded'] = [int(x[4:6]) for x in X.date_recorded]
    
    # change data types
    X['region_code'] = X['region_code'].astype('object')
    X['district_code'] = X['district_code'].astype('object')
    X['permit'] = X.permit.astype('bool')

    # adding features
    X['zero_tsh'] = np.where(X.amount_tsh == 0, 1, 0)
    X['extreme_tsh'] = np.where(X.amount_tsh > 3000, 1, 0)
    X['negative_gps_height'] = np.where(X.gps_height < 0, 1, 0)
    X['zero_gps_height'] = np.where(X.gps_height == 0, 1, 0)
    X['zero_private'] = np.where(X.num_private == 0, 1, 0)
    X['zero_population'] = np.where(X.population == 0, 1, 0)
    X['extreme_population'] = np.where(X.population > 3000, 1, 0)
    
    cond = [X.construction_year > 2005, 
            X.construction_year > 2000, 
            X.construction_year > 1990, 
            X.construction_year > 1980, 
            X.construction_year > 1970]
    vals = ['after05', '00s', '90s', '80s', '70s']

    X['year_built'] = np.select(cond, vals, 'others')

    # new column: n_wells_village
    with open('PKL/subvil_counts.pkl', 'rb') as fp:
        subvil_counts = pickle.load(fp)
    
    for pnt in X.subvillage:
        try: subvil_counts[pnt] += 1
        except: subvil_counts[pnt] = 1
        
    X['n_wells_village'] = [subvil_counts[x] for x in X.subvillage]
    
    
    # turn all texts into lower case
    for c in di.text_feats:
        X[c] = [x.lower() for x in X[c]]
    
    
    # make categories
    categories = list(X.select_dtypes('object').columns)
    X[categories] = X[categories].astype('category')
    
    # Fix funder/installer texts
    exclist = string.punctuation + string.digits
    # remove punctuations and digits
    
    table_ = str.maketrans(exclist, ' '*len(exclist))
    X.funder = [' '.join(x.translate(table_).split()) for x in X.funder]
    X.installer = [' '.join(x.translate(table_).split()) for x in X.installer]
    
    # first fix the ones we know
    str_isin = di.str_isin
    
    for k, v in str_isin.items():
        X.funder = np.where(X.funder.isin(v), k, X.funder)
        
    str_includes = {'villages': 'vill', 'community': 'comm'}
    
    for k, v in str_includes.items():
        X.funder = np.where(v in X.funder, k, X.funder)
    
    for k, v in str_isin.items():
        X.installer = np.where(X.installer.isin(v), k, X.installer)
        
    for k, v in str_includes.items():
        X.installer = np.where(v in X.installer, k, X.installer)
        
    with open('PKL/funders.txt', 'rb') as filepath:
        funders = pickle.load(filepath)
    with open('PKL/installerss.txt', 'rb') as filepath:
        installers = pickle.load(filepath)
    
    X.installer = np.where(X.installer.isin(installers), 
                           X.installer, 'others')
    X.funder = np.where(X.funder.isin(funders), 
                           X.funder, 'others')   
    


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
    
    # turn ones without info as others
    
    with open('PKL/lgas.pkl', 'rb') as fp:
        lga_list = pickle.load(fp)
   
    X['lga'] = np.where(X.lga.isin(lga_list), X.lga, 'others')    

    # separate out urban and rural wards
    X['urban_wards'] = X.ward.str.contains('urban')
    X['rural_wards'] = X.ward.str.contains('rural')   
    
    with open('PKL/extraction_type_c.pkl', 'rb') as fp:
        extraction_type_list = pickle.load(fp)
        
    # add the extraction type class
    X['extraction_type_c'] = np.where(X.extraction_type.isin(extraction_type_list), X.extraction_type, X.extraction_type_group)
    
    # final columns
    cols = ['amount_tsh', 'funder', 'gps_height', 'installer', 'longitude',
       'latitude', 'num_private', 'basin', 'region', 'district_code', 'lga',
       'population', 'public_meeting', 'scheme_management', 'permit',
       'construction_year', 'management', 'payment_type', 'water_quality',
       'quantity', 'source', 'waterpoint_type',
       'year_recorded', 'month_recorded', 'zero_tsh', 'extreme_tsh',
       'negative_gps_height', 'zero_gps_height', 'zero_private', 'year_built',
       'zero_population', 'extreme_population', 'n_wells_village', 'basin_lat',
       'basin_long', 'dist_to_basin', 'lga_lat', 'lga_long', 'dist_to_lga',
       'urban_lga', 'rural_lga', 'urban_wards', 'rural_wards',
       'extraction_type_c']
    
    return X[cols]
    
    
    
    
    
    
    
    