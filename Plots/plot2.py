# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:40:18 2020

@author: Barbara
"""

import numpy as np
import pandas as pd
from functions import *
import matplotlib.pyplot as plt

''' When running the plots, comment the print lines of matches function in functions.py '''

indi = list(sc.index)  # Index for running through SWEET-Cat

sc2nasa=[]  # NASA
sc2eu=[]  # EU

for i in indi:
    NA, EU = match(sc_name=sc['name'][i])  # match all the SC stars with stars on NASA and EU
    if len(NA)!=0:
        if len(NA)>1:  # If a star has more than on planet, the star index will appear repeated
            for k in NA.index:
                sc2nasa.append([i,k])  
        else:     # Star only has one planet
            sc2nasa.append([i,NA.index[0]])
    
    if len(EU)!=0:
        if len(EU)>1:   # If a star has more than on planet, the star ind will appear repeated
            for j in EU.index:
                sc2eu.append([i,j])
        else:     # Star only has one planet
            sc2eu.append([i,EU.index[0]])

# From list to array
sc2nasa = np.array(sc2nasa)
sc2eu = np.array(sc2eu)

nasa_mass=[]
nasa_msini=[]
for i in range(len(sc2nasa)): # Apply condition for mass and precision in NASA
    if (na['pl_bmassj'][sc2nasa[i,1]]<0.094399)&((na['pl_bmassjerr1'][sc2nasa[i,1]]<0.2*na['pl_bmassj'][sc2nasa[i,1]])&(na['pl_bmassjerr2'][sc2nasa[i,1]]<0.2*na['pl_bmassj'][sc2nasa[i,1]])):
        nasa_mass.append([sc2nasa[i,0],sc2nasa[i,1]]) # list[SC_index, NASA_index]
        
    if (na['pl_bmsinij'][sc2nasa[i,1]]<0.094399)&((na['pl_bmsinijerr1'][sc2nasa[i,1]]<0.2*na['pl_bmsinij'][sc2nasa[i,1]])&(na['pl_bmsinijerr2'][sc2nasa[i,1]]<0.2*na['pl_bmsinij'][sc2nasa[i,1]])):
        nasa_msini.append([sc2nasa[i,0],sc2nasa[i,1]])# list[SC_index, NASA_index]

nasa_mass = np.array(nasa_mass)
nasa_msini = np.array(nasa_msini)
SC_NA = np.concatenate((nasa_mass[:,0],nasa_msini[:,0]))
NA_ind = np.concatenate((nasa_mass[:,1],nasa_msini[:,1]))

eu_mass = []  # Mass for EU
eu_msini = []   # Msini for EU

for j in range(len(sc2eu)):
    # Apply condition for mass and precision in EU
    if (eu['mass'][sc2eu[j,1]]<0.094399)&((eu['mass_error_max'][sc2eu[j,1]]<0.2*eu['mass'][sc2eu[j,1]])&(eu['mass_error_min'][sc2eu[j,1]]<0.2*eu['mass'][sc2eu[j,1]])):
        eu_mass.append([sc2eu[j,0],sc2eu[j,1]])
        
    if (eu['mass_sini'][sc2eu[j,1]]<0.094399)&((eu['mass_sini_error_max'][sc2eu[j,1]]<0.2*eu['mass_sini'][sc2eu[j,1]])&(eu['mass_sini_error_min'][sc2eu[j,1]]<0.2*eu['mass_sini'][sc2eu[j,1]])):
        eu_msini.append([sc2eu[j,0],sc2eu[j,1]])
        
eu_mass = np.array(eu_mass)
eu_msini = np.array(eu_msini)

# Remove repeated indexes
idx_eu = list(set(eu_mass[:,1])^set(eu_msini[:,1])) 

# Indexes of mass for EU
# Choose mass and not msini but few of them are still minimum masses in EU
# Remove msini values
msini_eu = np.intersect1d(eu_msini[:,1],idx_eu)  
 
# Sort msini_eu as eu_msini[:,1] was, to not lose information
m2 = np.array(sorted(list(msini_eu), key=list(eu_msini[:,1]).index)) 

# Remove the stars for which some mass indexes were removed
df = pd.DataFrame(eu_msini)
df2 = df.loc[df[1].isin(m2)]
eu_msini2 = np.array(df2)

EU_ind = np.concatenate((eu_mass[:,1],eu_msini2[:,1]))  # Indexes for EU
SC_EU = np.concatenate((eu_mass[:,0],eu_msini2[:,0]))

# First indexes for NASA, second for EU
sc_ind = np.concatenate((SC_NA,SC_EU))  # Indexes for SWEET-Cat

' Metallicity'
#feh = sc['feh'][sc_ind]
feh = sc['feh'][eu_msini2[:,0]]

' Period '
#per = pd.concat([na.loc[NA_ind,'pl_orbper'],eu.loc[EU_ind,'orbital_period']])
#per = pd.concat([eu.loc[eu_mass[:,1],'orbital_period'], eu.loc[eu_msini2[:,1],'orbital_period']])
per = pd.concat([eu.loc[eu_msini2[:,1],'orbital_period']])

' Mass '
#m = pd.concat([na['pl_bmassj'][nasa_mass[:,1]]*317.8, na['pl_bmsinij'][nasa_msini[:,1]]*317.8, eu['mass'][eu_mass[:,1]]*317.8, eu['mass_sini'][eu_msini2[:,1]]*317.8])
#m = pd.concat([eu['mass'][eu_mass[:,1]]*317.8, eu['mass_sini'][eu_msini2[:,1]]*317.8])
m = pd.concat([eu['mass_sini'][eu_msini2[:,1]]*317.8])


'''PLOT'''
' SCATTER PLOT ' 

x2 = feh
y2 = per
t2 = m
fig, (ax1) = plt.subplots(1)
map1 = ax1.scatter(x2, y2, c=t2, cmap='viridis')
fig.colorbar(map1, ax=ax1, label = r'Mass ($M_{\oplus}$)')
plt.xlabel('Stellar metallicity [Fe/H]')
plt.ylabel('Period (days)')
plt.yscale('log')
plt.grid(True)
plt.savefig('period-metal-mass.pdf',format='pdf')
plt.show()



#' HISTOGRAM '
#plt.hist(m,bins=30,orientation='horizontal',ec='black',alpha=0.7)
#plt.ylabel('Mass')
#plt.xlabel('Number os planets')
#plt.show()