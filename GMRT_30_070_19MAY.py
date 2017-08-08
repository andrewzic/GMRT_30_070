import os
import shutil
import time
from  astropy.time import Time
import astropy.units as u

execfile('/import/extreme2/azic/phd/GMRT_30_070/GMRT_pipeline_azic.py')


"""
initial setup - filenames, creating directories for this run etc.
"""

path = '/import/extreme2/azic/phd/GMRT_30_070/'

now = time.strftime('%Y%m%d_%H%M%S') #iso format
casadir = '%s/19may/%s/' %(path,now) #all CASA-generated files (logs, flag tables, caltables, etc. will go in here
plotpath = '%splots/' %casadir
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


os.mkdir('%scasaplots/%s/' %(path,now))
for f in os.listdir(casadir):
    if f[-3:]=='.ms' or 'plots' in f:
        #continue
        pass
    if f[-4:]=='.png':
        shutil.copyfile(f, '%scasaplots/%s/' %(path,now))
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

execfile('%sGMRT_30_070_19MAY.setup.py' %path)

casadir = '%s/19may/%s/' %(path,now) #reset casadir which is redefined in the setup script.

"""
import the data by copying the original split 16s-averaged ms into casadir
"""
print original_msname
print msname
shutil.copytree(original_msname, msname)

"""
flagging data
"""
print("""intial flagging!""")
initial_flagging(msname)
flag_stats(msname, note = 'INITIAL FLAGGING')
print("""manual flagging""")
manual_flagging(msname, manual_flags)
flag_stats(msname, note = 'MANUAL FLAGGING')
print("""auto tfcrop flagging""")
auto_tf_flagging(msname)
flag_stats(msname, note = 'AUTO TFCROP FLAGGING')

"""
initial bandpass
"""

iter_num = 0
bp_spwin = '0:150~170'
ref_ant = 'C03' #reference antenna for phase calibrations


while iter_num < 1:

    init_bandpass(msname, minsnr, flux_cal_name, ref_ant, caldir, iter_num, spwin = bp_spwin, flux_cal_scan = '1')

    auto_r_flagging(msname, fields = '0,1') #just the calibrator sources
    
    iter_num += 1

iter_num_final = iter_num

print("""
final calibrations
""")

default('clearcal')
clearcal(vis = msname)
setjy_res = init_setjy(msname, flux_cal_name) #set flux density scale

bandpass_name = final_bandpass(msname, minsnr, flux_cal_name, ref_ant, caldir, iter_num_final, spwin = bp_spwin, flux_cal_scan = '1') #final bandpass calibration

print("""
beginning gain calibration pass 1. 
Refant is %s
""" %ref_ant)

#determine antenna gains for each calibrator source
final_gaincal(msname, minsnr, flux_cal_name, flux_cal_name, ref_ant, caldir, iter_num_final, False, bandpass_name, field_scan = '1')
print("""
beginning gain calibration pass 2. 
Refant is %s
""" %ref_ant)
gaincal_name = final_gaincal(msname, minsnr, phase_cal_name, flux_cal_name, ref_ant, caldir, iter_num_final, True, bandpass_name)


'''
#polarisation calibration
print("""
beginning polarisation calibration. 
Refant is %s
""" %ref_ant)
pol_cal_name = '3C286'
pol_cal_2_name = 'J1513+2338'
caldir = casadir
iter_num = 1
minsnr = 3.0


polcal_name, polcal2_name, polcal3_name = final_polcal(msname, minsnr, pol_cal_name, pol_cal_2_name, ref_ant, caldir, iter_num, gaincal_name, bandpass_name, pol_cal_scan = '1')
'''

#bootstrap flux density for target source:
fluxcal_name = final_fluxscale(msname, [flux_cal_name], [phase_cal_name], caldir, gaincal_name)

print("""applying final calibrations
""")
#apply final calibrations

gaintables = [bandpass_name, fluxcal_name]#, polcal_name, polcal2_name, polcal3_name]
interps = ['', '']#, '', '', ''] #last 3 are for polcal

for s in [flux_cal_name, phase_cal_name]:
    gainfields = [flux_cal_name, s]
    final_applycal(msname, s, gaintables, interps, gainfields, par_ang = True)


####
#now apply calibrations to target
###

gainfields = [flux_cal_name, phase_cal_name] #, polcal_name, polcal2_name, polcal3_name]
interps = ['', 'linear', '', '', '']

final_applycal(msname, target_name, gaintables, interps, gainfields)


'''
#now image each field
for s_key in field_dict:
    s_name = field_dict[s_key]
    if s_name == 'J1314+1320':
        continue
    
    if s_name == '3C286':
        image_scan = '1'
    else:
        image_scan = ''
    
    print("""
***********
Imaging %s!
***********
""" %s_name)

    threshold = 3.0*field_rms[s_key]
    
    image(s_name,
          msname,
          casadir,
          1000,
          threshold,
          scan = image_scan,
          interactive = True,
          im_size = [n_pix, n_pix],
          cell_size = pixel_size,
          stokes = 'I',
          weighting = 'natural',
          usescratch = False)
'''


#inspect data after it has been calibrated
for s, cal_scan in zip([flux_cal_name, phase_cal_name], ['1', '']):#, target_name]:
    diagnostic_plotms(msname, caldir, s, flux_cal_scan = cal_scan)

