# -*- coding: utf-8 -*-
"""
Created on Wed May 13 20:15:13 2020

@author: Barbara
"""
import numpy as np
import pandas as pd
from funcoes import *
import matplotlib.pyplot as plt

## Mass < 30 Mt NASA + error < 20 %
m_na, = np.where((na['pl_bmassj']<0.094399)&((na['pl_bmassjerr1']<0.2*na['pl_bmassj'])&(na['pl_bmassjerr2']<0.2*na['pl_bmassj'])))
# Msini < 30 Mt NASA + error < 20 %
mi_na, = np.where((na['pl_bmsinij']<0.094399)&((na['pl_bmsinijerr1']<0.2*na['pl_bmsinij'])&(na['pl_bmsinijerr2']<0.2*na['pl_bmsinij'])))
#Mi_na = list(mi_na) # --> indices

idx_na = np.concatenate([m_na,mi_na])

# Caracteristicas dos planetas com M<30 erro<20%
R_NA = na.loc[idx_na,'ra']  # Coordinates RA
D_NA = na.loc[idx_na,'dec']  # Coordinates DEC


ra,dec=coor2deg()  # Coordenadas do SC em graus

nomatch =[]
ind_nasa_sc =[]
for a in idx_na:
    q, = np.where((abs(R_NA[a]-ra)<(5/3600)) & (abs(D_NA[a]-dec)<(5/3600)))
    if len(q)==0:
        nomatch.append([na['pl_hostname'][a],a])
        # save nomatch as list with a
    else:
        # save list of the found indexes q (in SWEETCat) and respective a
        ind_nasa_sc.append([a,q[0]])
nomatch_na = np.array(nomatch)        
ind_na=np.array(ind_nasa_sc)[:,0]
ind_sc1=np.array(ind_nasa_sc)[:,1]
    
# --------------------------------
## Mass < 30 Mt NASA + error < 20 %
m_eu, = np.where((eu['mass']<0.094399)&((eu['mass_error_max']<0.2*eu['mass'])&(eu['mass_error_min']<0.2*eu['mass'])))
# Msini < 30 Mt NASA + error < 20 %
mi_eu, = np.where((eu['mass_sini']<0.094399)&((eu['mass_sini_error_max']<0.2*eu['mass_sini'])&(eu['mass_sini_error_min']<0.2*eu['mass_sini'])))

# There are some planets with both mass and mass sini.
idx_eu = list(set(m_eu)^set(mi_eu)) # Remove repeated indexes
m_eu2 = np.intersect1d(m_eu,idx_eu)  # Mass except repeated indexes

ra2,dec2=coor2deg()

R_EU = eu.loc[idx_eu,'ra'].astype(float) # Coordinates RA (EU has them in str)
D_EU = eu.loc[idx_eu,'dec'].astype(float)  # Coordinates DEC (EU has them in str)

nomatch2 =[]
ind_eu_sc =[]
for e in idx_eu:
    u, = np.where((abs(R_EU[e]-ra2)<(5/3600)) & (abs(D_EU[e]-dec2)<(5/3600)))
    if len(u)==0:
        nomatch2.append([eu['name'][e],e])
        # save nomatch as list with a
    else:
        # save list of the found indexes q (in SWEETCat) and respective a
        ind_eu_sc.append([e,u[0]])
nomatch_eu = np.array(nomatch2)        
ind_eu=np.array(ind_eu_sc)[:,0]
ind_sc2=np.array(ind_eu_sc)[:,1]

ind_sc=np.concatenate((ind_sc1,ind_sc2))


'QUANTITIES'
feh = sc['feh'][ind_sc]
per = pd.concat([na['pl_orbper'][ind_na],eu['orbital_period'][ind_eu]])
m1 = np.intersect1d(ind_na,m_na) # mass NASA
m2 = np.intersect1d(ind_na,mi_na) # mass sini NASA
m3 = np.intersect1d(ind_eu,m_eu2) # mass EU
m4 = np.intersect1d(ind_eu,mi_eu) # mass sini EU
m = pd.concat([na['pl_bmassj'][m1]*317.8,na['pl_bmsinij'][m2]*317.8,eu['mass'][m3]*317.8,eu['mass_sini'][m4]*317.8])

MT = pd.concat([na['pl_bmassj']*317.8,na['pl_bmsinij']*317.8,eu['mass']*317.8,eu['mass_sini']*317.8])

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

' HISTOGRAMA '
plt.hist(m,bins=30,orientation='horizontal',ec='black',alpha=0.7)
#plt.hist(MT[~np.isnan(MT)],orientation='horizontal',ec='black',alpha=0.3)
plt.ylabel('Mass')
plt.xlabel('Number os planets')
plt.show()
##################################################

#from numpy import corrcoef, sum, log, arange
#from numpy.random import rand
#from pylab import pcolor, show, colorbar, xticks, yticks
#
## generating some uncorrelated data
#data = rand(10,100) # each row of represents a variable
#
## creating correlation between the variables
## variable 2 is correlated with all the other variables
#data[2,:] = sum(data,0)
## variable 4 is correlated with variable 8
#data[4,:] = log(data[8,:])*0.5
#
## plotting the correlation matrix
#R = corrcoef(data)
#pcolor([m,m])
#colorbar()
##yticks(arange(min(m),max(m)),range(int(min(m)),int(max(m))))
##xticks(arange(min(m),max(m)),range(int(min(m)),int(max(m))))
#show()