# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 20:59:09 2020

@author: Barbara
"""

import numpy as np
import pandas as pd
from nasa import get_data as ndata

def new_na():
    # NASA original database
    na = pd.DataFrame.from_dict(ndata())
    
    # Find which rows are mass*sini
    Indx, = np.where(na['pl_bmassprov']=='Msini')
    indx = list(Indx)
    zeros = np.zeros((1,len(indx)))
    zeros[:] = np.nan
    empty = list(zeros[0])
    
    N = len(na)
    msin = np.zeros((1,N))[0]
    msin[:] = np.nan
    msin1 = np.zeros((1,N))[0]
    msin1[:] = np.nan
    msin2 = np.zeros((1,N))[0]
    msin2[:] = np.nan
    
    
    
    msin[indx] = na['pl_bmassj'][indx]
    na.at[indx,'pl_bmassj'] = empty
    Msin = list(msin)
    
    msin[indx] = na['pl_bmassjerr1'][indx]
    na.at[indx,'pl_bmassjerr1'] = empty
    Msin_err1 = list(msin)
    
    msin[indx] = na['pl_bmassjerr2'][indx]
    na.at[indx,'pl_bmassjerr2'] = empty
    Msin_err2 = list(msin)
    
    na.insert(loc=29, column='pl_bmsinij', value=Msin)
    na.insert(loc=30, column='pl_bmsinijerr1', value=Msin_err1)
    na.insert(loc=31, column='pl_bmsinijerr2', value=Msin_err2)
    
    return na