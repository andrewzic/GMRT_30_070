import os
import shutil
import time

execfile('/import/extreme2/azic/phd/GMRT_30_070/GMRT_pipeline_azic.py')


"""
initial setup - filenames, creating directories for this run etc.
"""

path = '/import/extreme2/azic/phd/GMRT_30_070/'

now = time.strftime('%d%m%Y_%H%M%S')
casadir = '%sCASA/%s/' %(path,now) #all CASA-generated files (logs, flag tables, caltables, etc. will go in here
plotpath = casadir + 'plots/'
if not os.path.exists(casadir):
    os.mkdir(casadir)
#    
os.chdir(casadir)
print('''
Files being saved in:
%s
''' %casadir)

print('''
*********************************
PURGING ALL CASA FILES IN CASADIR
*********************************
''')


os.mkdir(path+'casaplots/%s/' %now)
for f in os.listdir(casadir):
    if f[-3:]=='.ms' or 'plots' in f:
        #continue
        pass
    if f[-4:]=='.png':
        shutil.copyfile(f, path+'casaplots/%s/' %now)
    f_path = os.path.join(casadir,f)
    try:
        if os.path.isfile(f_path):
            os.unlink(f_path)
        elif os.path.isdir(f_path):
            shutil.rmtree(f_path)
    except Exception as e:
        print(e)

os.mkdir(plotpath)

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
"""
#applycal can't find tables if not in same dir as ms file
caldir = casadir + flux_cal_name + '_cal/'
if not os.path.exists(caldir):
    os.mkdir(caldir)
"""
caldir = casadir
refant = 'C05' #reference antenna for phase calibrations
minsnr = 3.0

int_time = 16.1061

"""
import the data:
"""
import_data(datafile, flagfile, msname)

"""
flagging data
"""
initial_flagging(msname)
flag_stats(msname, note = 'INITIAL FLAGGING')
manual_flagging(msname, manual_flags)
flag_stats(msname, note = 'MANUAL FLAGGING')
auto_tf_flagging(msname)
flag_stats(msname, note = 'AUTO TFCROP FLAGGING')


"""
initial bandpass
"""

iter_num = 0

# while iter_num < 1:

#     init_bandpass(msname, minsnr, flux_cal_name, refant, caldir, iter_num)

#     #auto_r_flagging(msname)
    
#     iter_num += 1

iter_num_final = 1 #iter_num

print("""
final calibrations
""")

default('clearcal')
clearcal(vis = msname)
setjy_res = init_setjy(msname, flux_cal_name) #set flux density scale
bandpass_name = final_bandpass(msname, minsnr, flux_cal_name, refant, caldir, iter_num_final) #final bandpass calibration


#determine antenna gains for each calibrator source
final_gaincal(msname, minsnr, flux_cal_name, flux_cal_name, refant, caldir, iter_num_final, False, bandpass_name)
final_gaincal(msname, minsnr, phase_cal_name, flux_cal_name, refant, caldir, iter_num_final, True, bandpass_name)
gaincal_name = final_gaincal(msname, minsnr, flux_cal_2_name, flux_cal_name, refant, caldir, iter_num_final, True, bandpass_name)

#bootstrap flux density for target source:
fluxcal_name = final_fluxscale(msname, [flux_cal_name], [phase_cal_name, flux_cal_2_name], caldir, gaincal_name)
print("""applying final calibrations
""")
#apply final calibrations

gaintables = [bandpass_name, fluxcal_name]
interps = ['', '']

for s in [flux_cal_name, phase_cal_name, flux_cal_2_name]:
    gainfields = [flux_cal_name, s]
    final_applycal(msname, s, gaintables, interps, gainfields)


####
#now apply calibrations to target
###

gainfields = [flux_cal_name, phase_cal_name]
interps = ['', 'linear']

final_applycal(msname, target_name, gaintables, interps, gainfields)

cell_size = 0.51 #arcsec
expected_rms_cal = 0.263 #mJy
expected_rms_target = 0.05 #around this mark
clean_threshold_cal  = 3.0*expected_rms_cal
clean_threshold_target = 0.1 #3.0*expected_rms_target

#now image each field
for s_key in field_dict:
    
    s_name = field_dict[s_key]
    
    if s_name == 'TVLM513-46':
        threshold = '%fmJy' %clean_threshold_target
    else:
        threshold = '%fmJy' %clean_threshold_cal
        continue
        
    image(s_name,
          msname,
          casadir,
          15000,
          threshold,
          interactive = True,
          im_size = [4096, 4096],
          cell_size = 0.51,
          stokes = 'I',
          weighting = 'natural',
          usescratch = True)



#inspect data after it has been calibrated
for s in [flux_cal_name, phase_cal_name]:#, target_name]:
    diagnostic_plotms(msname, caldir, s)




