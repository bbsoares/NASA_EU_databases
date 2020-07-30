# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 12:22:47 2020

@author: Barbara
"""

# dictionary EU --> NASA
# Note that there are parameters from EU that don't have any correspondence in NASA (and vice versa)
dic = {'name':'pl_name','planet_status':'','mass':'pl_bmassj',
       'mass_error_min':'pl_bmassjerr2','mass_error_max':'pl_bmassjerr1',
       'mass_sini':'pl_bmsinij','mass_sini_error_min':'pl_bmsinijerr2',
       'mass_sini_error_max':'pl_bmsinijerr1',
       'radius':'pl_radj', 'radius_error_min':'pl_radjerr2', 
       'radius_error_max':'pl_radjerr1', 'orbital_period':'pl_orbper', 
       'orbital_period_error_min':'pl_orbpererr2', 'orbital_period_error_max':'pl_orbpererr1', 
       'semi_major_axis':'pl_orbsmax', 'semi_major_axis_error_min':'pl_orbsmaxerr2', 
       'semi_major_axis_error_max':'pl_orbsmaxerr1', 'eccentricity':'pl_orbeccen', 
       'eccentricity_error_min':'pl_orbeccenerr2', 'eccentricity_error_max':'pl_orbeccenerr1', 
       'inclination':'pl_orbincl', 'inclination_error_min':'pl_orbinclerr2', 
       'inclination_error_max':'pl_orbinclerr1', 'angular_distance':'', 'discovered':'', 
       'updated':'rowupdate', 'omega':'', 'omega_error_min':'', 
       'omega_error_max':'', 'tperi':'', 'tperi_error_min':'', 'tperi_error_max':'', 
       'tconj':'', 'tconj_error_min':'', 'tconj_error_max':'', 'tzero_tr':'', 'tzero_tr_error_min':'',
       'tzero_tr_error_max':'', 'tzero_tr_sec':'', 'tzero_tr_sec_error_min':'',
       'tzero_tr_sec_error_max':'', 'lambda_angle':'', 'lambda_angle_error_min':'',
       'lambda_angle_error_max':'', 'impact_parameter':'',
       'impact_parameter_error_min':'', 'impact_parameter_error_max':'', 'tzero_vr':'',
       'tzero_vr_error_min':'', 'tzero_vr_error_max':'', 'k':'', 'k_error_min':'',
       'k_error_max':'', 'temp_calculated':'', 'temp_calculated_error_min':'',
       'temp_calculated_error_max':'', 'temp_measured':'', 'hot_point_lon':'',
       'geometric_albedo':'', 'geometric_albedo_error_min':'',
       'geometric_albedo_error_max':'', 'log_g':'', 'publication':'', 'detection_type':'pl_discmethod',
       'mass_detection_type':'', 'radius_detection_type':'', 'alternate_names':'',
       'molecules':'', 'star_name':'pl_hostname', 'ra':'ra', 'dec':'dec', 'mag_v':'', 'mag_i':'', 'mag_j':'',
       'mag_h':'', 'mag_k':'', 'star_distance':'st_dist', 'star_distance_error_min':'st_disterr2',
       'star_distance_error_max':'st_disterr1', 'star_metallicity':'',
       'star_metallicity_error_min':'', 'star_metallicity_error_max':'', 'star_mass':'st_mass',
       'star_mass_error_min':'st_masserr2', 'star_mass_error_max':'st_masserr1', 'star_radius':'st_rad',
       'star_radius_error_min':'st_raderr2', 'star_radius_error_max':'st_raderr1', 'star_sp_type':'',
       'star_age':'', 'star_age_error_min':'', 'star_age_error_max':'', 'star_teff':'st_teff',
       'star_teff_error_min':'st_tefferr2', 'star_teff_error_max':'st_tefferr1', 'star_detected_disc':'',
       'star_magnetic_field':'', 'star_alternate_names':''}
