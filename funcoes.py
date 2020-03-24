# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 00:12:44 2020

@author: Barbara
"""

import numpy as np
import pandas as pd
from nasa import get_data

na = pd.DataFrame.from_dict(nasa.get_data())
#print(na.iloc[:,0:2])
# na['pl_hostname'][na['pl_hostname'] == 'KOI-12'].index[0]

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
    # param has to be the name of the column
    st, = np.where(na['pl_hostname'] == star_name)
    lt, = np.where(na['pl_letter'] == letter)
    row = np.intersect1d(st,lt)
    par = na.loc[row,param]
    return par

## Example: find the radius of the planet Qatar-6 b:
# find_par_nasa('Qatar-6','b','pl_radj')