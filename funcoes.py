# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 00:12:44 2020

@author: Barbara
"""

import numpy as np
import pandas as pd
from nasa import get_data as ndata
from pyexoplaneteu import get_data as eudata

names_ = ['name', 'hd', 'ra', 'dec', 'V', 'Verr', 'p', 'perr',
                  'pflag', 'Teff', 'Tefferr', 'logg', 'logger',
                  'n1', 'n2', 'vt', 'vterr', 'feh', 'feherr', 'M', 'Merr',
                  'author', 'link', 'source', 'update', 'comment', 'database',
                  'n3']

na = pd.DataFrame.from_dict(ndata())
eu = pd.DataFrame.from_dict(eudata())
sc = pd.read_csv('WEBSITE_online_EU-NASA_full_database_clean_06-04-2020.rdb', sep='	', header=None, names=names_)
#pd.read_rdb()
#-----------------------------------------------------------------
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

####################################################################################################

def coor2deg():
    ''' Converts all RA and DEC SWEETCat coordinates to degrees '''

    RAsc = []
    DECsc = []
    
    for r in sc['ra']:
        ra_sc = (float(r[0:2])+float(r[3:5])/60.+float(r[6:])/3600.)*15.
        RAsc.append(ra_sc)
        
    for d in sc['dec']:
        if d[0] == '-':
            dec_sc = float(d[0:3])-float(d[4:6])/60.-float(d[7:])/3600.
            DECsc.append(dec_sc)
        else:
            dec_sc = float(d[0:3])+float(d[4:6])/60.+float(d[7:])/3600.
            DECsc.append(dec_sc)
    
    return np.array(RAsc), np.array(DECsc)
    

def coor_sc2deg(star_name):
    ''' The user gives the name of the star as it is in the SWEETCat database.
        Converts coordinates of the star to degrees '''
    
    # Coordinates of SWEETCat in hh:mm:ss
    ra_sc_ = (sc[(sc['name']==star_name)][['ra']]).values[0,0]
    dec_sc_ = (sc[(sc['name']==star_name)][['dec']]).values[0,0]
    
    # Change the coordinates from hh:mm:ss to degrees
    ra_sc = (float(ra_sc_[0:2])+float(ra_sc_[3:5])/60.+float(ra_sc_[6:])/3600.)*15.
    if dec_sc_[0] == '-':
        dec_sc = float(dec_sc_[0:3])-float(dec_sc_[4:6])/60.-float(dec_sc_[7:])/3600.
    else:
        dec_sc = float(dec_sc_[0:3])+float(dec_sc_[4:6])/60.+float(dec_sc_[7:])/3600.
    
    return ra_sc,dec_sc



        
##############################################################################
    
def match(sc_name, lim=0.09):
    ''' Given the SWEETCat name of a star, verifies if
    it already exists in the NASA and EU database.
    If so,  returns all related information. The checking
    is done for coordinates and with a certain limit. '''
    
    RAsc, DECsc = coor_sc2deg(sc_name)
    
    # The coordinates on EU database are strings --> convert to float
    ra=[]
    dec=[]
    results=[]
    param=[]
    
    for i in eu['ra']:
        ra.append(float(i))
    for j in eu['dec']:
        dec.append(float(j))
    
    for exo in [na,eu]:
        # If we are checking the EU database, we need to use the float values and not the string ones
        if len(exo)==len(eu):
            exo['ra']=np.array(ra)
            exo['dec']=np.array(dec)
            
        # Compare values. It's a match if the difference between them is less than 0.0900
        ind, = np.where((abs(RAsc-exo['ra'])<lim) & ((abs(DECsc-exo['dec']))<lim))

        # Which database are we checking?
        if len(exo)==len(na):
            if len(ind)==0:
                print('No match found')
            else:
                print('\n Star in both SWEETCat and NASA databases. Found',str(len(ind)),'matche(s): \n')
        
        if len(exo)==len(eu):
            if len(ind)==0:
                print('No match found')
            else:
                print('\n Star in both SWEETCat and EU databases. Found',str(len(ind)),'matche(s): \n')
        results.append(ind)
        for e in ind:
            print(exo.iloc[e],'\n')
            param.append(exo.iloc[e])
    return 'NASA index matches: '+str(results[0])+'  EU index matche(s) '+str(results[1])


#----------------------------------------------------------------------------------------------------------

def match2(sc_name, lim= 0.09):
    ''' Given the SWEETCat name of a star, uses the
    database column and returns all related information
    from the respective database of the star and its planets. '''
    
    RAsc, DECsc = coor_sc2deg(sc_name)
    
    # The coordinates on EU database are strings --> convert to float
    ra=[]
    dec=[]
    results=[]
    
    for i in eu['ra']:
        ra.append(float(i))
    for j in eu['dec']:
        dec.append(float(j))
    
    indx, = np.where(sc['name']==sc_name)[0]
#    print(indx)
    db = sc['database'][indx]
#    print(str(db))
    if db=='EU':
        param = []
        RA=np.array(ra)
        DEC=np.array(dec)
        ind, = np.where((abs(RAsc-RA)<lim) & ((abs(DECsc-DEC))<lim))
        print('\n Star in both SWEETCat and EU databases. Found',str(len(ind)),'matche(s).')
        for h in ind:
            param.append(eu.iloc[h])
        
    
    if db=='EU,NASA':
        param = []
        for exo in [eu,na]:
            # If we are checking the EU database, we need to use the float values and not the string ones
            if len(exo)==len(eu):
                exo['ra']=np.array(ra)
                exo['dec']=np.array(dec)
            
            # Compare values. It's a match if the difference between them is less than lim
            ind, = np.where((abs(RAsc-exo['ra'])<lim) & ((abs(DECsc-exo['dec']))<lim))
    
            # Which database are we checking?
            if len(exo)==len(na):
                print('\n Star in both SWEETCat and NASA databases. Found',str(len(ind)),'matche(s).')
            
            if len(exo)==len(eu):
                print('\n Star in both SWEETCat and EU databases. Found',str(len(ind)),'matche(s).')
            
            results.append(ind)
            for e in ind:
                param.append(exo.iloc[e])
                
    if db=='NASA':
        param = []
        ind, = np.where((abs(RAsc-na['ra'])<lim) & ((abs(DECsc-na['dec']))<lim))
        print('\n Star in both SWEETCat and NASA databases. Found',str(len(ind)),'matche(s).')
        for h in ind:
            param.append(eu.iloc[h])
    return param, '\n', db

#-----------------------------------------------------------------------
print(sc['M'][3048], eu['mass'][4237], na['pl_bmassj'][4132])