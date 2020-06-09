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
    NA, EU = match(sc['name'][i])
    if len(NA)!=0:
        if len(NA)>1:
            for k in NA.index:
                t1.append([i,k])
        else:
            t1.append([i,NA.index[0]])
    
#        scna.append([i,list(NA.index)])
    if len(EU)!=0:
        if len(NA)>1:
            for j in EU.index:
                t2.append([i,j])
        else:
            t2.append([i,EU.index[0]])

t1=np.array(t1)
na_ind = t1[:,1]
sc2na = t1[:,0]

t2=np.array(t2)
eu_ind = t2[:,1]
sc2eu = t2[:,0]

nam=[]
nami=[]
for i in range(len(na_ind)):
    if (na['pl_bmassj'][na_ind[i]]<0.094399)&((na['pl_bmassjerr1'][na_ind[i]]<0.2*na['pl_bmassj'][na_ind[i]])&(na['pl_bmassjerr2'][na_ind[i]]<0.2*na['pl_bmassj'][na_ind[i]])):
        nam.append([sc2na[i],na_ind[i]])
    if (na['pl_bmsinij'][na_ind[i]]<0.094399)&((na['pl_bmsinijerr1'][na_ind[i]]<0.2*na['pl_bmsinij'][na_ind[i]])&(na['pl_bmsinijerr2'][na_ind[i]]<0.2*na['pl_bmsinij'][na_ind[i]])):
        nami.append([sc2na[i],na_ind[i]])

nam=np.array(nam)
nami=np.array(nami)
SC_NA=np.concatenate((nam[:,0],nami[:,0]))

m_na = nam[:,1]
mi_na = nami[:,1]
NA_ind=np.concatenate((mi_eu,m_eu2))


eum=[]
eumi=[]
for j in range(len(eu_ind)):
    if (eu['mass'][eu_ind[j]]<0.094399)&((eu['mass_error_max'][eu_ind[j]]<0.2*eu['mass'][eu_ind[j]])&(eu['mass_error_min'][eu_ind[j]]<0.2*eu['mass'][eu_ind[j]])):
        eum.append([sc2eu[j],eu_ind[j]])
    if (eu['mass_sini'][eu_ind[j]]<0.094399)&((eu['mass_sini_error_max'][eu_ind[j]]<0.2*eu['mass_sini'][eu_ind[j]])&(eu['mass_sini_error_min'][eu_ind[j]]<0.2*eu['mass_sini'][eu_ind[j]])):
        eumi.append([sc2eu[j],eu_ind[j]])
        
eum=np.array(eum)
eumi=np.array(eumi)
SC_EU=np.concatenate((eum[:,0],eumi[:,0]))

m_eu = eum[:,1]
mi_eu = eumi[:,1]   # Indexes of msini for EU
idx_eu = list(set(m_eu)^set(mi_eu)) # Remove repeated indexes
m_eu2 = np.intersect1d(m_eu,idx_eu)  # Indexes of mass for EU

sc_ind = np.concatenate((SC_EU,SC_NA))
EU_ind=np.concatenate((mi_eu,m_eu2))


feh = sc['feh'][sc_ind]
per = pd.concat([na.loc[NA_ind,'pl_orbper'],eu.loc[EU_ind,'orbital_period']])
m = pd.concat([na['pl_bmassj'][m_na]*317.8,na['pl_bmsinij'][mi_na]*317.8,eu['mass'][m_eu2]*317.8,eu['mass_sini'][mi_eu]*317.8])


'PLOT'
x = feh
y = per
t = m
fig, (ax1) = plt.subplots(1)
map1 = ax1.scatter(x, y, c=t, cmap='viridis')
fig.colorbar(map1, ax=ax1)
plt.xlabel('Stellar metallicity [Fe/H]')
plt.ylabel('Period (days)')
plt.show()


## np.array(set(sc2na)^set(indi))
## subset of planetary parameters dataframe SC-EU, SC-NASA
# na.loc[nai]
# eu.loc[eui]