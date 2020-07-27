# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 00:12:44 2020

@author: Barbara
"""
import numpy as np
import pandas as pd
from new_nasa import new_na
from pyexoplaneteu import get_data as eudata
from dictio import dic

names_ = ['name', 'hd', 'ra', 'dec', 'V', 'Verr', 'p', 'perr',
                  'pflag', 'Teff', 'Tefferr', 'logg', 'logger',
                  'n1', 'n2', 'vt', 'vterr', 'feh', 'feherr', 'M', 'Merr',
                  'author', 'link', 'source', 'update', 'comment', 'database',
                  'n3']

na = new_na()
eu = pd.DataFrame.from_dict(eudata())
sc = pd.read_csv('WEBSITE_online_EU-NASA_full_database_clean_06-04-2020.rdb', sep='	', header=None, names=names_)

#-----------------------------------------------------------------

def coor_sc2deg(star_name):
    ''' The user gives the name of the star as it is in the SWEETCat database.
        Converts coordinates of the star to degrees. '''
    
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


    
def match(sc_name, lim=5, list_of_parameters=None):
    ''' Given the SWEETCat name of a star, verifies if
    it already exists in the NASA and EU database.
    If so,  returns all related information. The checking
    is done for coordinates and with a certain limit.
    
    sc_name: star name as it is in SWEETCat
    lim: limit used to compare coordinates, in arcsec
    list_of_parameters: parameters of the planet(s) we want
    to see. None by default shows all parameters. Parameters
    be as in EU database. Run eu.columns to see options. '''
    
    # Name is in SWEETCat?
    if len(sc[sc['name']==sc_name])==0:
        raise Exception('This name does not exist in SWEETCat. Please write a star present in SWEETCat.')
    else:
        pass
    
    rasc, decsc = coor_sc2deg(sc_name)  # Coordinates are in degrees
    
    # Convert coordinates to arcseconds
    RAsc=rasc*3600
    DECsc=decsc*3600
    
    # The coordinates on EU database are strings --> convert to float
    ra=[]
    dec=[]
    results=[]
    
    for i in eu['ra']:
        ra.append(float(i))
    for j in eu['dec']:
        dec.append(float(j))
    
    for exo in [na,eu]:
        # In the EU database, we need to convert the string values to float
        if len(exo)==len(eu):
            exo['ra']=np.array(ra)
            exo['dec']=np.array(dec)
            
        # Compare values. It's a match if the difference between them is less than 5 arcseconds.
        # Coordinates are in degrees, multiply for 3600 to convert to arcseconds.
        ind, = np.where((abs(RAsc-exo['ra']*3600)<lim) & ((abs(DECsc-exo['dec']*3600))<lim))
        
        
        # Which database are we checking?
        if len(exo)==len(na):  # Checking NASA
            if len(ind)==0:  # No match for coordinates!
                
                # If coordinates don't work, try checking by name
                inx, = np.where(na['pl_hostname']==sc_name)
                results.append(inx)
                
                if len(inx)==0:
                    print('No match found in NASA.')
                    NA = na.loc[list(inx)]
                    
                else:
                    print('Match by name in NASA.')
                    if list_of_parameters==None:
                        NA = na.loc[list(inx)]
                        
                    else:
                        # Find corresponding column name in NASA
                        params = [dic.get(key) for key in list_of_parameters]
                        
                        # Parameters that don't exist in NASA, only EU
                        no, = np.where(np.array(params)=='')
                        dont = [list_of_parameters[z] for z in no]
                        print('The following parameter(s) do(es) not exist in NASA:',str(dont))
                        
                        # Parameters common in EU and NASA
                        yes, = np.where(np.array(params)!='')
                        na_params = [params[i] for i in yes]
                        NA = na.loc[list(inx),na_params]

                    
            else:  # Match found by coordinates!
                results.append(ind)
                
                if list_of_parameters==None:  # Return all information
                    NA = na.loc[list(ind)]
                    
                else:
                    # Find corresponding column name in NASA
                    params = [dic.get(key) for key in list_of_parameters]
                    
                    # Parameters that don't exist in NASA, only EU
                    no, = np.where(np.array(params)=='')
                    dont = [list_of_parameters[z] for z in no]
                    print('The following parameter(s) do(es) not exist in NASA:',str(dont))
                    
                    # Parameters common in EU and NASA
                    yes, = np.where(np.array(params)!='')
                    na_params = [params[i] for i in yes]
                    NA = na.loc[list(ind),na_params]
        
        
        if len(exo)==len(eu):  # Checking EU
            if len(ind)==0:   # No match for coordinates!
                
                # If coordinates don't work, try checking by name
                inx, = np.where(eu['star_name']==sc_name)
                results.append(inx)

                if len(inx)==0:
                    print('No match found in EU.')
                    EU = eu.loc[list(inx)]
                    
                else:
                    print('Match by name in EU.')
                    if list_of_parameters==None:
                        EU = eu.loc[list(inx)]
                    else:
                        EU = eu.loc[list(inx),list_of_parameters]
            
            else:   # Match by coordinates found
                results.append(ind)
                if list_of_parameters==None:
                    EU = eu.loc[list(ind)]
                else:
                    EU = eu.loc[list(ind),list_of_parameters]

    print('NASA index matches: '+str(results[0])+'  EU index matche(s) '+str(results[1])+'\n')
    return NA, EU

#%%----------------------------------------------------------------------------

def verify_database(sc_name):
    ''' Given the SWEETCat name of a star, uses the
    database column of SWEET-Cat and returns all related information
    from the respective database of the star and its planets. '''

    # Name is in SWEETCat?
    if len(sc[sc['name']==sc_name])==0:
        raise Exception('This name does not exist in SWEETCat. Please write a star present in SWEETCat.')
    else:
        pass
    
    indx, = np.where(sc['name']==sc_name)[0]
    
    # Using database column
    db = sc['database'][indx]
    return db

#%%----------------------------------------------------------------------------
    
def get_sc(sc_name,list_of_parameters=None):
    ''' Give name of the star and parameters as they are in SWEETCat.
    Run sc.columns to see parameters avaiable. '''
    
    # Name is in SWEETCat?
    if len(sc[sc['name']==sc_name])==0:
        raise Exception('This name does not exist in SWEETCat. Please write a star present in SWEETCat.')
    else:
        pass
    
    # Get SWEET-Cat information
    # if there is a list of parameters
    if list_of_parameters==None:
        SC = sc[sc['name']==sc_name]
    
    # otherwise all information
    else:   
        SC = sc[sc['name']==sc_name][list_of_parameters]
    return SC

#%%----------------------------------------------------------------------------
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