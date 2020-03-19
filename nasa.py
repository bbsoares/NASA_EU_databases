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
import csv
from collections import OrderedDict

# the link in the "Download Data" button
download_link = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets'

# to get the directory where NASA Archive data will be stored
def _create_data_dir():
    """ Create empty directory where nasa.csv will be stored """
    home = os.path.expanduser("~")
    directory = os.path.join(home, '.nasaarchive')
    if not os.path.exists(directory):
        os.makedirs(directory)


def _check_data_dir():
    home = os.path.expanduser("~")
    directory = os.path.join(home, '.nasaarchive')
    return os.path.exists(directory)


def get_data_dir():
    """ Return directory where nasa.csv is stored """
    if not _check_data_dir():
        _create_data_dir()
        
    home = os.path.expanduser("~")
    return os.path.join(home, '.nasaarchive')

#########

def download_data():
    """ Download NASA Archive data and save it to `nasa.csv` """

    with request.urlopen(download_link) as response:
       data = response.read()

    local_file = os.path.join(get_data_dir(), 'nasa.csv')
    with open(local_file, 'wb') as f:
        f.write(data)

    print(f'Saved NASA Archive data to {local_file}')


def check_data_age():
    """ How old is `nasa.csv`, in days """
    local_file = os.path.join(get_data_dir(), 'nasa.csv')
    age = time.time() - os.path.getmtime(local_file) # in sec
    return age / (60*60*24) # in days


class DataDict(dict):
    numpy_entries = False

    __doc__ = "nasa_archive: a catalog of parameters for known exoplanets.\n" + \
              "The catalog and more information can be found " \
              "at https://exoplanetarchive.ipac.caltech.edu/\n" + \
              "This dictionary has the catalog columns as its keys; " \
              "see the `.columns()` method.\n" + \
              "Entries are lists, see `to_numpy()` to convert them to numpy arrays."

    def __init__(self, *args, **kwargs):
        super(DataDict, self).__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        # allows to do data[0] to get all columns for the 0th entry in the table
        if isinstance(key, int):
            return {k:v[key] for k, v in self.items()}


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
    def _repr_pretty_(self, p, cycle):
        return p.text(self.__repr__())

    def __len__(self):
        return len(self.__getitem__('pl_hostname'))

    def columns(self):
        """ List the available columns """
        pprint.pprint(list(self.keys()), compact=True)

    @property
    def size(self):
        return len(self.__getitem__('pl_hostname'))

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

    # Convert the values in integers
    def apply_int_to_column(data, key):
        data[key] = [int(v) for v in data[key]]

    # Convert values to float and replace empty values by NaN
    def apply_float_to_column(data, key):
        data[key] = [float(v) if v!='' else math.nan for v in data[key]]

    # read the file
    local_file = os.path.join(get_data_dir(), 'nasa.csv')
    with open(local_file) as csvfile:
        reader = csv.DictReader(csvfile)
        lines = [row for row in reader]

    # lines is a list of (ordered) dicts; transform it to a (ordered) dict of lists
    data = OrderedDict({k: [dic[k] for dic in lines] for k in lines[0]})

    # column labels were read automatically by the csv.DictReader
    labels = list(data.keys())

    nlab, nlin = len(labels), len(lines)
    print(f'There are {nlab} columns with {nlin} entries each in `nasa.csv`')

    data = DataDict(**data)

    # transform columns to integers or floats or keep the strings
    for col in data.keys():
        try:
            apply_int_to_column(data, col)
        except ValueError:
            try:
                apply_float_to_column(data, col)
            except ValueError:
                pass

    return data



def get_data():
    local_file = os.path.join(get_data_dir(), 'nasa.csv')

    if not os.path.exists(local_file):
        print ('Downloading NASA data')
        download_data()
    
    age = check_data_age()
    if age > 5:
        print ('Data in `nasa.csv` is older than 5 days, downloading.')
        download_data()
    else:
        print ('Data in `nasa.csv` is recent.')

    data = read_data()
    return data


if __name__ == '__main__':
    data = get_data()
