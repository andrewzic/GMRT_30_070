import os
import shutil
import time

execfile('/import/extreme2/azic/phd/GMRT_30_070/GMRT_pipeline_azic.py')


"""
initial setup - filenames, creating directories for this run etc.
"""

path = '/import/extreme2/azic/phd/GMRT_30_070/'


casadir = '%sCASA/final/' %path

os.chdir(casadir)
print('''
Files being saved in:
%s
''' %casadir)


"""
initialising important info
"""

prefix = '30_070_25SEP2016.LTA_RRLL.RRLLFITS' #filename prefix to use

datafile = path+prefix+'.fits' #the raw data
msname = casadir+prefix+'.ms' #the output measurement set ms file name
flagfile = path+'30_070_25sep2016.lta##30_070.FLAGS.4' #flagfile name
manual_flags = path + 'GMRT_30_070.flags.py'
plotpath = casadir + '/plots/'
flux_cal = '3'
flux_cal_2 = '0'
phase_cal = '1'
field_dict = {'0': '3C286', '1': 'J1513+2338', '2': 'TVLM513-46', '3': '3C48'}
phase_cal_name = field_dict[phase_cal]
flux_cal_name = field_dict[flux_cal]
flux_cal_2_name = field_dict[flux_cal_2]
target = '2'
target_name = field_dict[target]

caldir = casadir
refant = 'C05' #reference antenna for phase calibrations
minsnr = 3.0


cell_size = 0.51 #arcsec
expected_rms_cal = 0.263 #mJy
expected_rms_target = 0.05 #around this mark
clean_threshold_cal  = 3.0*expected_rms_cal
clean_threshold_target = 0.1 #3.0*expected_rms_target
