# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 00:12:44 2020

@author: Barbara
"""

import numpy as np
import pandas as pd
from nasa import get_data
import pysweetcat


na = pd.DataFrame.from_dict(get_data())
sc = pd.DataFrame.from_dict(pysweetcat.get_data())
#print(na.iloc[:,0:2])
# na['pl_hostname'][na['pl_hostname'] == 'KOI-12'].index[0]
# NOTA: exoplanet.eu tem RA e DEC em hh:mm:ss

def find_mass_nasa(star_name, letter):
    # array with the rows which have the star name
    st, = np.where(na['pl_hostname'] == star_name)
    # array with the rows which have the letter
    lt, = np.where(na['pl_letter'] == letter)
    # find the common element.
    # [This function could be rewritten if we give
    # the planet name as an argument. This implies that
    # for all systems, the star and the planet should
    # have the same name (could fail sometime)]
    row = np.intersect1d(st,lt)
    mass = na.loc[row,'pl_bmassj']
    return mass

## Example: find the mass of the planet HD 202696 b:
# find_mass_nasa('HD 202696','b')

def find_par_nasa(star_name, letter, param):
    # param has to be the name of the column (or a list of columns' names)
    st, = np.where(na['pl_hostname'] == star_name)
    lt, = np.where(na['pl_letter'] == letter)
    row = np.intersect1d(st,lt)
    par = na.loc[row,param]
    return par

## Example: find the radius of the planet Qatar-6 b:
# find_par_nasa('Qatar-6','b','pl_radj')
    
def coor(star_name, letter):
    ''' Returns the coordinates of the planet '''
    ra = (na[(na['pl_hostname']==star_name)&(na['pl_letter']==letter)][['ra']]).values[0][0]
    dec = na[(na['pl_hostname']==star_name)&(na['pl_letter']==letter)][['dec']].values[0][0]
    return ra, dec

def coor_nasa_sc(star_name, letter):
    ''' The user gives the name of the star as is in the SWEETCat database.
        Compare if the star exists in NASA database. 
        -- Unfinished yet. '''
    
    # Coordinates of SWEETCat in hh:mm:ss
    ra_sc_ = (sc[(sc['name']==star_name)][['ra']]).values[0][0]
    dec_sc_ = (sc[(sc['name']==star_name)][['dec']]).values[0][0]
    
    # Change the coordinates from hh:mm:ss to degrees
    ra_sc = (float(ra_sc_[0:2])+float(ra_sc_[3:5])/60.+float(ra_sc_[6:])/3600.)*15.
    if dec_sc_[0] == '-':
        dec_sc = float(dec_sc_[0:3])-float(dec_sc_[4:6])/60.-float(dec_sc_[7:])/3600.
    else:
        dec_sc = float(dec_sc_[0:3])+float(dec_sc_[4:6])/60.+float(dec_sc_[7:])/3600.
    
    # We want to see if these coordinates already exist in NASA database
    
    return ra_sc,dec_sc