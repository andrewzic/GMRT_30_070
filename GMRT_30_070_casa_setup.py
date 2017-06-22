import os
import shutil
import time

execfile('/import/extreme2/azic/phd/GMRT_30_070/GMRT_pipeline_azic.py')


"""
initial setup - filenames, creating directories for this run etc.
"""

path = '/import/extreme2/azic/phd/GMRT_30_070/'


casadir = '%sCASA/22062017_122645/' %path

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

###
#obs info
###

obs_date = '2016-09-25'

scan_start_times = {'1': '08:53:13.8', '2': '09:12:17.4', '3': '09:20:52.8', '4': '09:52:17.2', '5': '10:00:52.6', '6': '10:31:44.8', '7': '10:40:04.1', '8': '11:11:28.5', '9': '11:19:31.7', '10': '11:50:40.0', '11': '11:58:59.3', '12': '12:30:07.6', '13': '12:38:10.8', '14': '13:09:35.2', '15': '13:17:38.4', '16': '13:48:46.7', '17': '13:57:06.0', '18': '14:28:14.3', '19': '14:36:33.6', '20': '15:04:28.6', '21': '15:18:58.3'}

scan_end_times = {'1': '09:05:18.6', '2': '09:17:07.3', '3': '09:50:40.5', '4': '09:57:07.1', '5': '10:30:40.4', '6': '10:36:34.7', '7': '11:09:51.9', '8': '11:16:02.3', '9': '11:49:19.5', '10': '11:55:29.9', '11': '12:28:47.1', '12': '12:34:57.5', '13': '13:08:14.7', '14': '13:14:09.0', '15': '13:47:26.2', '16': '13:53:36.6', '17': '14:26:53.8', '18': '14:32:48.1', '19': '15:02:19.8', '20': '15:09:18.5', '21': '15:31:35.3'}

#2440000.5
int_time = 16.1061
#18 integrations for phase cal (4.8317 minutes)
#111 integrations for target (29.795 minutes)

cell_size = 0.51 #arcsec
expected_rms_cal = 0.263 #mJy
expected_rms_target = 0.05 #around this mark
clean_threshold_cal  = 3.0*expected_rms_cal
clean_threshold_target = 0.1 #3.0*expected_rms_target
