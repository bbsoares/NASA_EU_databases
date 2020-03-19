# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 19:28:16 2020

@author: Barbara
"""

#!/usr/bin/env python
import os
from urllib import request
import time
import math
import pprint

# the link in the "Download Data" button
download_link = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets'

# to get the directory where NASA Archive data will be stored
def _create_data_dir():
    """ Create empty directory where NASA.tsv will be stored """
    home = os.path.expanduser("~")
    directory = os.path.join(home, '.nasaarchive')
    if not os.path.exists(directory):
        os.makedirs(directory)


def _check_data_dir():
    home = os.path.expanduser("~")
    directory = os.path.join(home, '.nasaarchive')
    return os.path.exists(directory)


def get_data_dir():
    """ Return directory where NASA.tsv is stored """
    if not _check_data_dir():
        _create_data_dir()
        
    home = os.path.expanduser("~")
    return os.path.join(home, '.nasaarchive')

#########

def download_data():
    """ Download NASA Archive data and save it to `NASA.tsv` """

    with request.urlopen(download_link) as response:
       data = response.read()

    local_file = os.path.join(get_data_dir(), 'NASA.tsv')
    with open(local_file, 'wb') as f:
        f.write(data)

    print(f'Saved NASA Archive data to {local_file}')


def check_data_age():
    """ How old is `NASA.tsv`, in days """
    local_file = os.path.join(get_data_dir(), 'NASA.tsv')
    age = time.time() - os.path.getmtime(local_file) # in sec
    return age / (60*60*24) # in days


class DataDict(dict):
    numpy_entries = False

    __doc__ = "SWEET-Cat: a catalog of stellar parameters for stars with planets\n"+\
              "The catalog and more information can be found at www.astro.up.pt/resources/sweet-cat\n"+\
              "This dictionary has the same fields as keys "+\
              "(note that 'sigma' and 'pi' can be used instead of 'σ' and 'π')\n"+\
              "Entries are lists, see `to_numpy()` to convert them to numpy arrays."

    def __getitem__(self, key):
        # allows to do data[0] to get all columns for the 0th entry in the table
        if isinstance(key, int):
            return {k:v[key] for k, v in self.items()}

        # allows to do data['sigma_feh'] to get data['σ_feh']
        key = key.replace('sigma', 'σ').replace('pi', 'π')
        
        # allows to do data['key_nonan'] to get data['key'] without NaNs
        if key.endswith('_nonan'):
            val = super().__getitem__(key.replace('_nonan',''))
            try:
                if self.numpy_entries:
                    from numpy import isnan
                    val = val[~isnan(val)]
                else:
                    val = [v for v in val if not math.isnan(v)]
            except TypeError:
                # this column does not have floats
                pass
        else:
            val = super().__getitem__(key)

        return val

    def __str__(self):
        return 'NASA Archive data'
    def __repr__(self):
        return f'NASA Archive data: dictionary with {self.size} entries. '+\
                'Use .columns() to get the column labels.'
                
    def __len__(self):
        return len(self.__getitem__('name'))

    def columns(self):
        """ List the available columns """
        pprint.pprint(list(self.keys()), compact=True)

    @property
    def size(self):
        return len(self.__getitem__('name'))

    def to_numpy(self, inplace=True):
        """ 
        Convert entries to numpy arrays. If `inplace` is True convert
        the entries in place, else return a new dictionary.
        """
        from numpy import asarray # this assumes numpy is installed
        newself = self if inplace else DataDict()
        for k, v in self.items():
            newself[k] = asarray(v)
        newself.numpy_entries = True
        if not inplace:
            return newself


def read_data():
    def val2float(val):
        if val == '':
            return math.nan
        try: 
            return float(val)
        except ValueError:
            return val
    def val2int(val):
        try: 
            return int(val)
        except ValueError:
            return val

#    labels = ['name', 'HD', 
#              'ra', 'dec', 'vmag', 'σ_vmag', 'π', 'σ_π', 'source_π',
#              'teff', 'σ_teff', 'logg', 'σ_logg', 'LC_logg', 'σ_LC_logg',
#              'vt', 'σ_vt', 'feh', 'σ_feh', 'mass', 'σ_mass', 'reference',
#              'homogeneity', 'last_update', 'comments']
    
    labels = ['pl_hostname','pl_letter','pl_name','pl_discmethod', 'pl_controvflag',
              'pl_pnum','pl_orbper','pl_orbpererr1','pl_orbpererr2','pl_orbperlim',
              'pl_orbpern','pl_orbsmax','pl_orbsmaxerr1','pl_orbsmaxerr2','pl_orbsmaxlim',
              'pl_orbsmaxn','pl_orbeccen','pl_orbeccenerr1','pl_orbeccenerr2','pl_orbeccenlim',
              'pl_orbeccenn','pl_orbincl','pl_orbinclerr1','pl_orbinclerr2','pl_orbincllim',
              'pl_orbincln','pl_bmassj','pl_bmassjerr1','pl_bmassjerr2','pl_bmassjlim',
              'pl_bmassn','pl_bmassprov','pl_radj','pl_radjerr1','pl_radjerr2',
              'pl_radjlim','pl_radn','pl_dens','pl_denserr1','pl_denserr2',
              'pl_denslim','pl_densn','pl_ttvflag','pl_kepflag','pl_k2flag',
              'ra_str','dec_str','ra','st_raerr','dec',
              'st_decerr','st_posn','st_dist','st_disterr1','st_disterr2',
              'st_distlim','st_distn','st_optmag','st_optmagerr','st_optmaglim',
              'st_optband','gaia_gmag','gaia_gmagerr','gaia_gmaglim','st_teff',
              'st_tefferr1','st_tefferr2','st_tefflim','st_teffn','st_mass',
              'st_masserr1','st_masserr2','st_masslim','st_massn','st_rad',
              'st_raderr1','st_raderr2','st_radlim','st_radn','pl_nnotes',
              'rowupdate','pl_facility']

    # empty dictionary to save data
    data = {label:[] for label in labels}

    # read the file
    local_file = os.path.join(get_data_dir(), 'NASA.tsv')
    lines = open(local_file).readlines()

    nlab, nlin = len(labels), len(lines)
    print(f'There are {nlab} columns with {nlin} entries each in `NASA.tsv`')

    for line in lines:
        # split the columns
        vals = line.strip().split(',')
        # make some columns into ints
        vals = vals[:4] + list(map(val2int, vals[4:6])) + list(map(val2int, vals[9:11])) \
        + list(map(val2int, vals[14:16])) + list(map(val2int, vals[19:21])) \
        + list(map(val2int, vals[24:26])) + list(map(val2int, vals[29:32])) \
        + list(map(val2int, vals[35:37])) + list(map(val2int, vals[40:47])) \
        + list(map(val2int, vals[51])) + list(map(val2int, vals[55:57])) \
        + list(map(val2int, vals[59:61])) + list(map(val2int, vals[63])) \
        + list(map(val2int, vals[67:69])) + list(map(val2int, vals[72:74])) \
        + list(map(val2int, vals[77:]))
        
        # make some columns into floats
        vals[6:9] = list(map(val2float, vals[6:9]))
        vals[11:14] = list(map(val2float, vals[11:14]))
        vals[16:19] = list(map(val2float, vals[16:19]))
        vals[21:24] = list(map(val2float, vals[21:24]))
        vals[26:29] = list(map(val2float, vals[26:29]))
        vals[32:35] = list(map(val2float, vals[32:35]))
        vals[37:40] = list(map(val2float, vals[37:40]))
        vals[47:51] = list(map(val2float, vals[47:51]))
        vals[52:55] = list(map(val2float, vals[52:55]))
        vals[57:59] = list(map(val2float, vals[57:59]))
        vals[61:63] = list(map(val2float, vals[61:63]))
        vals[64:67] = list(map(val2float, vals[64:67]))
        vals[69:72] = list(map(val2float, vals[69:72]))
        vals[74:77] = list(map(val2float, vals[74:77]))

        for i, v in enumerate(data.values()):
            v.append(vals[i])

    data = DataDict(**data)
    return data


def get_data():
    local_file = os.path.join(get_data_dir(), 'NASA.tsv')

    if not os.path.exists(local_file):
        print ('Downloading NASA data')
        download_data()
    
    age = check_data_age()
    if age > 5:
        print ('Data in `NASA.tsv` is older than 5 days, downloading.')
        download_data()
    else:
        print ('Data in `NASA.tsv` is recent.')

    data = read_data()
    return data


if __name__ == '__main__':
    data = get_data()
