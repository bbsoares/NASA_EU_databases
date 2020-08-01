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


    
def match(sc_name=None, lim=5, list_of_parameters=None, r_asc=None, declin=None):
    ''' Given the SWEETCat name of a star or its coordinates, 
    verifies if it already exists in the NASA and EU database.
    If so, returns all related information or the parameters 
    specified. The checking is done by name or for coordinates and 
    within a certain limit.
    
    sc_name: star name as it is in SWEETCat (string)
    --> Case sensitive names!
    lim: limit used to compare coordinates, in arcsec (float)
    list_of_parameters: parameters of the planet(s) we want
    to see (list).
    --> None by default shows all parameters. Parameters should
        be given as in EU database. Run eu.columns to see options. 
    r_asc: right ascension coordinate of the star (string)
    declin: declination coordinate of the star (string)
    
    The user can choose to give the star's name OR its coordinates, 
    both as they are given in SWEETCat'''
    
    # Give the name of the star
    if sc_name!=None and r_asc==None and declin==None:
        
        # Name is in SWEETCat?
        if len(sc[sc['name']==sc_name])==0:
            raise Exception('This name does not exist in SWEETCat. Please write a star present in SWEETCat.')
        else:
            pass
        
        RAsc_deg, DECsc_deg = coor_sc2deg(sc_name)  # Coordinates are in degrees
        
        # Convert coordinates from degrees to arcseconds
        RAsc_arcsec=RAsc_deg*3600
        DECsc_arcsec=DECsc_deg*3600
    
    # Give the SWEETCat coordinates of the star
    elif sc_name==None and r_asc!=None and declin!=None:
        
        # Coordinates are in SWEETCat?
        if len(sc[sc['ra']==r_asc])==0 or len(sc[sc['dec']==declin])==0:
            raise Exception('These coordinates do not exist in SWEETCat. Please choose coordinates from SWEETCat.')
        else:
            pass
        
        # Convert coordinates from hh:mm:ss and dd:mm:ss to (degrees and then to) arcseconds
        RAsc_arcsec = ((float(r_asc[0:2])+float(r_asc[3:5])/60.+float(r_asc[6:])/3600.)*15.)*3600
        
        if declin[0] == '-':
            DECsc_arcsec = (float(declin[0:3])-float(declin[4:6])/60.-float(declin[7:])/3600.)*3600
        else:
            DECsc_arcsec = (float(declin[0:3])+float(declin[4:6])/60.+float(declin[7:])/3600.)*3600
    
        sc_name = sc[(sc['ra']==r_asc)&(sc['dec']==declin)]['name'].values[0]
    # Doesn't give name nor coordinates
    elif sc_name==None and ((r_asc!=None and declin==None) or (r_asc==None and declin!=None)):
        raise Exception('Please give BOTH right ascension and declination coordinates as they are in SWEETCat.')

    else:
        raise Exception('Please give the name of the star OR its coordinates as they are in SWEETCat.')
    
    
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
        # Coordinates of NASA and EU are in degrees, multiply for 3600 to convert to arcseconds.
        ind, = np.where((abs(RAsc_arcsec-exo['ra']*3600)<lim) & ((abs(DECsc_arcsec-exo['dec']*3600))<lim))
        
        
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
                    
                    # No list of parameters specified
                    if list_of_parameters==None:
                        NA = na.loc[list(inx)]
                        
                        # Change columns' names to be equal to EU (more readable names)
                        old_col=[val for key,val in dic.items() if val!='']
                        new_col = [key for key,val in dic.items() if val!='']
                        NA.rename(columns=dict(zip(old_col, new_col)), inplace=True)

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
                        
                        # Change columns' names to be equal to EU (more readable names)
                        new_name = [list(dic.keys())[list(dic.values()).index(nn)] for nn in na_params]
                        NA.rename(columns=dict(zip(na_params, new_name)), inplace=True)

                    
            else:  # Match found by coordinates!
                print('Match by coordinates in NASA.')
                results.append(ind)
                
                if list_of_parameters==None:  # Return all information
                    NA = na.loc[list(ind)]
                    
                    # Change columns' names to be equal to EU (more readable names)
                    old_col=[val for key,val in dic.items() if val!='']
                    new_col = [key for key,val in dic.items() if val!='']
                    NA.rename(columns=dict(zip(old_col, new_col)), inplace=True)
                    
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
                    
                    # Change columns' names to be equal to EU (more readable names)
                    new_name = [list(dic.keys())[list(dic.values()).index(nn)] for nn in na_params]
                    NA.rename(columns=dict(zip(na_params, new_name)), inplace=True)
        
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
                print('Match by coordinates in EU.')
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
    database column of SWEET-Cat to verify which database 
    contains information of the star and its planets. '''

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
    Run sc.columns to see parameters available.
    Alternatively, see names_ for parameters names in SWEETCat. '''
    
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

    RAsc_deg = []
    DECsc_deg = []
    
    for r in sc['ra']:
        ra_sc = (float(r[0:2])+float(r[3:5])/60.+float(r[6:])/3600.)*15.
        RAsc_deg.append(ra_sc)
        
    for d in sc['dec']:
        if d[0] == '-':
            dec_sc = float(d[0:3])-float(d[4:6])/60.-float(d[7:])/3600.
            DECsc_deg.append(dec_sc)
        else:
            dec_sc = float(d[0:3])+float(d[4:6])/60.+float(d[7:])/3600.
            DECsc_deg.append(dec_sc)
    
    return np.array(RAsc_deg), np.array(DECsc_deg)