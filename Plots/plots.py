# -*- coding: utf-8 -*-
"""
Created on Wed May 13 20:15:13 2020

@author: Barbara
"""
import numpy as np
import pandas as pd
from functions import *
import matplotlib.pyplot as plt

## Mass < 30 Mt NASA + error < 20 %
m_na, = np.where((na['pl_bmassj']<0.094399)&((na['pl_bmassjerr1']<0.2*na['pl_bmassj'])&(na['pl_bmassjerr2']<0.2*na['pl_bmassj'])))
# Msini < 30 Mt NASA + error < 20 %
mi_na, = np.where((na['pl_msinij']<0.094399)&((na['pl_msinijerr1']<0.2*na['pl_msinij'])&(na['pl_msinijerr2']<0.2*na['pl_msinij'])))
#Mi_na = list(mi_na) # --> indices


idx_na = list(set(m_na)^set(mi_na)) # Remove repeated indexes
mi_na2 = np.intersect1d(mi_na,idx_na)  # Mass except repeated indexes

# Sort mass_eu as eu_mass[:,1] was, to not lose information
mi_na2 = np.array(sorted(list(mi_na2), key=list(mi_na).index))

idx_na = np.concatenate([m_na,mi_na2])
# msini_notm = []
# for j in mi_na:
#     if j not in m_na:
#         msini_notm.append(j)
# for j in m_na:
#     if j not in mi_na:
#         msini_notm.append(j)
# # m_na = sort(m_na)
# msini_notm = np.array(msini_notm)
# idx_na = np.concatenate([m_na,msini_notm])

# Caracteristicas dos planetas com M<30 erro<20%
r_na = na.loc[idx_na,'ra']  # Coordinates RA
d_na = na.loc[idx_na,'dec']  # Coordinates DEC


ra,dec=coor2deg()  # Coordenadas do SC em graus

nomatch =[]
ind_nasa_sc =[]
for a in idx_na:
    q, = np.where((abs(r_na[a]-ra)<(5/3600)) & (abs(d_na[a]-dec)<(5/3600)))
    if len(q)==0:
        nomatch.append([na['hostname'][a],a])
        # save nomatch as list with index a
    else:
        # save list of the found indexes q (in SWEETCat) and respective index a
        ind_nasa_sc.append([a,q[0]])

nomatch_na = np.array(nomatch)        
ind_na=np.array(ind_nasa_sc)[:,0]
ind_sc1=np.array(ind_nasa_sc)[:,1]
    
#%%
## Mass < 30 Mt NASA + error < 20 %
m_eu, = np.where((eu['mass']<0.094399)&((eu['mass_error_max']<0.2*eu['mass'])&(eu['mass_error_min']<0.2*eu['mass'])))

# Msini < 30 Mt NASA + error < 20 %
mi_eu, = np.where((eu['mass_sini']<0.094399)&((eu['mass_sini_error_max']<0.2*eu['mass_sini'])&(eu['mass_sini_error_min']<0.2*eu['mass_sini'])))

# There are some planets with both mass and mass sini.
idx_eu = list(set(m_eu)^set(mi_eu)) # Remove repeated indexes
mi_eu2 = np.intersect1d(mi_eu,idx_eu)  # Mass except repeated indexes

# Sort mass_eu as eu_mass[:,1] was, to not lose information
mi_eu2 = np.array(sorted(list(mi_eu2), key=list(mi_eu).index))

# ra2,dec2=coor2deg()

r_eu = eu.loc[idx_eu,'ra'].astype(float) # Coordinates RA (EU has them in str)
d_eu = eu.loc[idx_eu,'dec'].astype(float)  # Coordinates DEC (EU has them in str)

nomatch2 =[]
ind_eu_sc =[]
for e in mi_eu2:
    u, = np.where((abs(r_eu[e]-ra)<(5/3600)) & (abs(d_eu[e]-dec)<(5/3600)))
    if len(u)==0:
        nomatch2.append([eu['name'][e],e])
        # save nomatch as list with index e
    else:
        # save list of the found indexes u (in SWEETCat) and respective index e
        ind_eu_sc.append([e,u[0]])

nomatch_eu = np.array(nomatch2)        
ind_eu=np.array(ind_eu_sc)[:,0]
ind_sc2=np.array(ind_eu_sc)[:,1]

ind_sc=np.concatenate((ind_sc1,ind_sc2))

'QUANTITIES'
feh = sc['[Fe/H]'][ind_sc]

per = pd.concat([na['pl_orbper'][ind_na],eu['orbital_period'][ind_eu]])
#per = eu['orbital_period'][m4]

m1 = np.intersect1d(ind_na,m_na) # mass NASA
m2 = np.intersect1d(ind_na,mi_na2) # mass sini NASA
m3 = np.intersect1d(ind_eu,m_eu) # mass EU
m4 = np.intersect1d(ind_eu,mi_eu2) # mass sini EU

# m = m1 + m2 + m3 + m4
m = pd.concat([na['pl_bmassj'][m1]*317.8,na['pl_msinij'][m2]*317.8,eu['mass'][m3]*317.8,eu['mass_sini'][m4]*317.8])
#m = eu['mass_sini'][m4]*317.8

# Total mass --> all High Mass and Low Mass Planets
MT = pd.concat([na['pl_bmassj']*317.8,na['pl_msinij']*317.8,eu['mass']*317.8,eu['mass_sini']*317.8])

'PLOT'
x = feh
y = per
t = m
fig, (ax1) = plt.subplots(1)
map1 = ax1.scatter(x, y, c=t, cmap='viridis')
fig.colorbar(map1, ax=ax1, label = 'Mass')
plt.xlabel('Stellar metallicity [Fe/H]')
plt.ylabel('Period (days)')
plt.yscale('log')
plt.show()


' HISTOGRAMA '
##A,B = np.histogram(m,bins=30)
##plt.hist(m,bins=np.logspace(np.log10(B[0]),np.log10(B[-1]),len(B)),orientation='horizontal',ec='black',alpha=0.9,zorder=0)
plt.figure()
plt.hist(m,bins=30,orientation='horizontal',ec='black',alpha=0.9)
##C,D = np.histogram(MT[~np.isnan(MT)],bins=30)
##plt.hist(MT[~np.isnan(MT)],bins=np.logspace(np.log10(D[0]),np.log10(D[-1]),len(D)),orientation='horizontal',ec='black',alpha=0.25)
plt.ylabel('Mass')
plt.xlabel('Number of planets')
#plt.yscale('log')
plt.show()
