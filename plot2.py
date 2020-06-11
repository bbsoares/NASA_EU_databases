# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:40:18 2020

@author: Barbara
"""

import numpy as np
import pandas as pd
from funcoes import *
import matplotlib.pyplot as plt

indi = list(sc.index)

t1=[]
t2=[]
for i in indi:
    NA, EU = match(sc['name'][i])  # match all the SC stars with stars on NASA and EU
    if len(NA)!=0:
        if len(NA)>1:  # If a star has more than on planet, the star ind will appear repeated
            for k in NA.index:
                t1.append([i,k])  
        else:     # Star only has one planet
            t1.append([i,NA.index[0]])
    
    if len(EU)!=0:
        if len(NA)>1:   # If a star has more than on planet, the star ind will appear repeated
            for j in EU.index:
                t2.append([i,j])
        else:     # Star only has one planet
            t2.append([i,EU.index[0]])

t1=np.array(t1)
#na_ind = t1[:,1]
#sc2na = t1[:,0]

t2=np.array(t2)
#eu_ind = t2[:,1]
#sc2eu = t2[:,0]

nam=[]
nami=[]
for i in range(len(t1)): # Apply condition for mass and precision in NASA
    if (na['pl_bmassj'][t1[i,1]]<0.094399)&((na['pl_bmassjerr1'][t1[i,1]]<0.2*na['pl_bmassj'][t1[i,1]])&(na['pl_bmassjerr2'][t1[i,1]]<0.2*na['pl_bmassj'][t1[i,1]])):
        nam.append([t1[i,0],t1[i,1]])
        
    if (na['pl_bmsinij'][t1[i,1]]<0.094399)&((na['pl_bmsinijerr1'][t1[i,1]]<0.2*na['pl_bmsinij'][t1[i,1]])&(na['pl_bmsinijerr2'][t1[i,1]]<0.2*na['pl_bmsinij'][t1[i,1]])):
        nami.append([t1[i,0],t1[i,1]])

nam=np.array(nam)
nami=np.array(nami)
SC_NA=np.concatenate((nam[:,0],nami[:,0]))
NA_ind=np.concatenate((nam[:,1],nami[:,1]))


eum=[]  # Mass for EU
eumi=[]   # Msini for EU
for j in range(len(t2)):  # Apply condition for mass and precision in EU
    if (eu['mass'][t2[j,1]]<0.094399)&((eu['mass_error_max'][t2[j,1]]<0.2*eu['mass'][t2[j,1]])&(eu['mass_error_min'][t2[j,1]]<0.2*eu['mass'][t2[j,1]])):
        eum.append([t2[j,0],t2[j,1]])
        
    if (eu['mass_sini'][t2[j,1]]<0.094399)&((eu['mass_sini_error_max'][t2[j,1]]<0.2*eu['mass_sini'][t2[j,1]])&(eu['mass_sini_error_min'][t2[j,1]]<0.2*eu['mass_sini'][t2[j,1]])):
        eumi.append([t2[j,0],t2[j,1]])
        
eum=np.array(eum)
eumi=np.array(eumi)

# Remove repeated indexes
idx_eu = list(set(eum[:,1])^set(eumi[:,1])) 
# Indexes of mass for EU
m_eu2 = np.intersect1d(eum[:,1],idx_eu)   
# Sort m_eu2 as eum[:,1] was to not lose information
m2=np.array(sorted(list(m_eu2), key=list(eum[:,1]).index)) 


# Remove the stars for which some mass indexes were removed
df = pd.DataFrame(eum)
df2 = df.loc[df[1].isin(m2)]
eum2 = np.array(df2)

EU_ind=np.concatenate((eum2[:,1],eumi[:,1]))  # Indexes for EU
SC_EU=np.concatenate((eum2[:,0],eumi[:,0]))
sc_ind = np.concatenate((SC_EU,SC_NA))  # Indexes for SWEET-Cat

# Metallicity
feh = sc['feh'][sc_ind]
# Period
per = pd.concat([na.loc[NA_ind,'pl_orbper'],eu.loc[EU_ind,'orbital_period']])
# Mass
m = pd.concat([na['pl_bmassj'][nam[:,1]]*317.8,na['pl_bmsinij'][nami[:,1]]*317.8,eu['mass'][eum2[:,1]]*317.8,eu['mass_sini'][eumi[:,1]]*317.8])


'''PLOT'''
' SCATTER PLOT ' 
x = feh
y = per
t = m
fig, (ax1) = plt.subplots(1)
map1 = ax1.scatter(x, y, c=t, cmap='viridis')
fig.colorbar(map1, ax=ax1, label = 'Mass')
plt.xlabel('Stellar metallicity [Fe/H]')
plt.ylabel('Period (days)')
plt.show()

' HISTOGRAM '
plt.hist(m,bins=30,orientation='horizontal',ec='black',alpha=0.7)
plt.ylabel('Mass')
plt.xlabel('Number os planets')
plt.show()


## np.array(set(sc2na)^set(indi))
## subset of planetary parameters dataframe SC-EU, SC-NASA
# na.loc[nai]
# eu.loc[eui]