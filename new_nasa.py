# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 20:59:09 2020

@author: Barbara
"""

import numpy as np
import pandas as pd
from nasa import get_data as ndata

def new_na():

    na = pd.DataFrame.from_dict(ndata())
    
    Indx, = np.where(na['pl_bmassprov']=='Msini')
    indx = list(Indx)
    zeros = list(np.zeros((1,len(indx)))[0])
    N = len(na)
    msin = np.zeros((1,N))[0]
    msin[:] = np.nan
    msin1 = np.zeros((1,N))[0]
    msin1[:] = np.nan
    msin2 = np.zeros((1,N))[0]
    msin2[:] = np.nan
    
    
    
    msin[indx] = na['pl_bmassj'][indx]
    na.at[indx,'pl_bmassj']=zeros
    Msin=list(msin)
    
    msin[indx] = na['pl_bmassjerr1'][indx]
    na.at[indx,'pl_bmassjerr1']=zeros
    Msin_err1=list(msin)
    
    msin[indx] = na['pl_bmassjerr2'][indx]
    na.at[indx,'pl_bmassjerr2']=zeros
    Msin_err2=list(msin)
    
    na.insert(loc=29 ,column='pl_bmsinj', value=Msin)
    na.insert(loc=30 ,column='pl_bmsinjerr1', value=Msin_err1)
    na.insert(loc=31 ,column='pl_bmsinjerr2', value=Msin_err2)
    
    return na