import os
import shutil
import time
import glob
from astropy.time import Time, TimeDelta
import astropy.units as u
#execfile('/import/extreme2/azic/phd/GMRT_30_070/GMRT_pipeline_azic.py')


"""
initial setup - filenames, creating directories for this run etc.
"""

path = '/import/extreme2/azic/phd/GMRT_30_070/'


casadir = sorted(glob.glob('%s19may/*2017*/' %path))[-1] #for now, i guess

os.chdir(casadir)
print('''
Files being saved in:
%s
''' %casadir)


"""
initialising important info
"""

old_prefix = '30_070_19MAY2016_2S.LTA_RRLL.RRLLFITS' #2s integrations
prefix = '30_070_19MAY2016_16S.LTA_RRLL.RRLLFITS' #filename prefix to use

datafile = path+old_prefix +'.fits' #the raw data
original_msname = path + '19may/' + prefix + '.ms' #original unflagged 16s-averaged dataset
msname = casadir + prefix + '.ms' #the output measurement set ms file name
flagfile = path + '30_070_19may2016_2s.lta##30_070.FLAGS.1' #flagfile name
manual_flags = path + 'GMRT_30_070_19MAY.flags.py'
plotpath = casadir + '/plots/'

field_dict = {'0': '3C286', '1': 'J1309+1154', '2': 'J1314+1320'}
flux_cal = '0'
phase_cal = '1'
target = '2'
flux_cal_name = field_dict[flux_cal]
phase_cal_name = field_dict[phase_cal]
target_name = field_dict[target]

caldir = casadir
ref_ant = 'C05' #reference antenna for phase calibrations
minsnr = 3.0

###
#obs info
###

obs_date = '2016-05-19'

scan_durations = {}

scan_start_times = {'11': '16:37:11.9', '10': '16:00:41.5', '13': '17:22:27.8', '12': '16:45:27.2', '15': '18:07:39.7', '14': '17:30:41.0', '17': '19:08:25.7', '16': '18:15:52.9', '18': '19:15:30.5', '1': '12:52:12.9', '0': '12:36:08.6', '3': '13:37:16.8', '2': '13:00:18.1', '5': '14:22:48.8', '4': '13:45:40.1', '7': '15:07:42.5', '6': '14:30:54.0', '9': '15:52:26.2', '8': '15:16:11.9'}

scan_end_times = {'11': '16:42:11.9', '10': '16:36:07.5', '13': '17:27:27.7', '12': '17:21:29.4', '15': '18:12:39.6', '14': '18:06:39.2', '17': '19:13:47.8', '16': '19:07:37.4', '18': '19:30:42.5', '1': '12:57:14.9', '0': '12:50:52.4', '3': '13:42:16.7', '2': '13:36:18.4', '5': '14:27:48.7', '4': '14:21:52.4', '7': '15:12:44.5', '6': '15:06:42.1', '9': '15:57:26.2', '8': '15:51:37.9'}

for scan in scan_start_times:
    scan_start = Time(obs_date + ' ' + scan_start_times[scan], format = 'iso')
    scan_end = Time(obs_date + ' ' + scan_end_times[scan], format = 'iso')
    scan_dt = (scan_end - scan_start).to(u.min)
    scan_durations[scan] = scan_dt

# field_durations = {}
# for key in field_dict:
#     field_duration[key] = 

#2440000.5
int_time = 8.0*2.0132 #16.1056s, averaged from original 2.0132s integrations

sp_res = 130.208 #spectral resolution, in kHz
bw = 33333.3 #bandwidth in kHz
start_freq = 1371.065 #starting frequency in MHz
central_freq = 1387.6667 #central freq in MHz
numchan = 256 #number of channels

#J1314+1320 coords
#'13h14m20.395960s', '+13d20m01.16195s' #from listobs file
ra = 198.584983167
dec = 13.3336560972

max_uvwave = 93873.4 #determined by looking at plotms
res_rad = 1.0/max_uvwave*u.rad #resolution in radians
res_arcsec = res_rad.to(u.arcsec) #resolution in arcsec
pixel_size = res_arcsec.value/5.0 #angular extent of pixels: 5 pixels per beam

fov_rad = 0.21/25.0*u.rad #lambda/D
fov_arcmin = fov_rad.to(u.arcmin)
n_pix = fov_arcmin/(pixel_size*u.arcsec.to(u.arcmin)) #around 3942
n_pix = int(2**(np.ceil(np.log(n_pix.value)/np.log(2.0)))) #round up to nearest power of 2

field_durations = {'0': 14.733, '1': 45.4283, '2': 302.62666} #durations for each field in minutes. field 0 only includes scan 1
field_rms = {'0': 0.215, '1': 0.123, '2': 0.0475} #expected RMS noise for each field in mJy

'''
expected_rms_flux_cal = 0.215 #mJy
clean_threshold_flux_cal = 2.0*expected_rms_flux_cal
phase_cal_duration = 45.4283 #minutes
#calculated with GMRT calc online, bw = 21, n_ant = 23, stokes = 1
expected_rms_phase_cal = 0.123 #mJy
clean_threshold_phase_cal = 2.0*expected_rms_phase_cal
expected_rms_target = 0.05 #around this mark
clean_threshold_cal  = 3.0*expected_rms_flux_cal
clean_threshold_target = 0.1 #3.0*expected_rms_target
'''
