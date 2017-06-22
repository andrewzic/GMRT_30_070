import os
import shutil
import time
from astropy.time import Time, TimeDelta
import astropy.units as u

execfile('/import/extreme2/azic/phd/GMRT_30_070/GMRT_pipeline_azic.py')
execfile('/import/extreme2/azic/phd/GMRT_30_070/GMRT_30_070_casa_setup.py')

# """
# initial setup - filenames, creating directories for this run etc.
# """

# path = '/import/extreme2/azic/phd/GMRT_30_070/'


# casadir = '%sCASA/final/' %path

# os.chdir(casadir)
# print('''
# Files being saved in:
# %s
# ''' %casadir)


# """
# initialising important info
# """

# prefix = '30_070_25SEP2016.LTA_RRLL.RRLLFITS' #filename prefix to use

# datafile = path+prefix+'.fits' #the raw data
# msname = casadir+prefix+'.ms' #the output measurement set ms file name
# flagfile = path+'30_070_25sep2016.lta##30_070.FLAGS.4' #flagfile name
# manual_flags = path + 'GMRT_30_070.flags.py'
# plotpath = casadir + '/plots/'
# flux_cal = '3'
# flux_cal_2 = '0'
# phase_cal = '1'
# field_dict = {'0': '3C286', '1': 'J1513+2338', '2': 'TVLM513-46', '3': '3C48'}
# phase_cal_name = field_dict[phase_cal]
# flux_cal_name = field_dict[flux_cal]
# flux_cal_2_name = field_dict[flux_cal_2]
# target = '2'
# target_name = field_dict[target]

# caldir = casadir
# refant = 'C05' #reference antenna for phase calibrations
# minsnr = 3.0


# cell_size = 0.51 #arcsec
# expected_rms_cal = 0.263 #mJy
# expected_rms_target = 0.05 #around this mark
# clean_threshold_cal  = 3.0*expected_rms_cal
# clean_threshold_target = 0.1 #3.0*expected_rms_target

'''
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
          weighting = 'natural')

'''
timebin = 8.0*int_time #128.8488 sec, average over exactly 8 integrations

split_msnames = []

for i in range(9):
    
    scan = str(3+2*i)
    
    print("""
    PROCESSING SCAN %i
    """ %int(scan))
    
    split_name = split_msname('30_070_uvsub.ms',
                              scan = scan,
                              timebin = '%fs' %timebin,
                              width = 256) #returns name of split ms file

    split_msnames.append(split_name)
    print split_name
    
    
    start_time = scan_start_times[scan] #start time of scan
    end_time = scan_end_times[scan] #end time of scan
    
    Start_Time = Time('%s %s' %(obs_date, start_time)) #start time of scan as astropy.time.Time object
    Image_Start_Time = Time('%s %s' %(obs_date, start_time)) #likewise for start time of image, initialise to Start_Time
    End_Time = Time('%s %s' %(obs_date, end_time)) #likewise for end time of scan

    Image_Duration = TimeDelta(timebin*u.s) #image duration as astropy.time.Time object
    
    print("""
    BEGINNING IMAGING IN TIME CHUNKS OF %f SECONDS
    """ %timebin)
    
    iter_num = 0
    while Image_Start_Time < End_Time:
        
        
        Image_Start_Time_dt = Image_Start_Time.datetime #datetime format
        image_start_time = '%.2i:%.2i:%04.1f' %(Image_Start_Time_dt.hour, Image_Start_Time_dt.minute, float(Image_Start_Time_dt.second) + Image_Start_Time_dt.microsecond*1.0E-6) #convert into CASA-friendly format
        

        Image_End_Time = Image_Start_Time + Image_Duration #end time of image
        
        Image_End_Time_dt = Image_End_Time.datetime #datetime format
        image_end_time = '%.2i:%.2i:%04.1f' %(Image_End_Time_dt.hour, Image_End_Time_dt.minute, float(Image_End_Time_dt.second) + Image_End_Time_dt.microsecond*1.0E-6) #convert image end time to CASA-friendly format

        timerange = '%s~%s' %(image_start_time, image_end_time) #finally give the timerange as casa is expecting it

        print("""
        TIMERANGE IS %s
        
        BEGGINING IMAGING ON %s
        """ %(timerange, split_name))
        #image using uvsub image
        image('TVLM513-46',
              split_name,
              casadir,
              10000,
              '1mJy', #3*0.588 mJy threshold for 23 antennas, 21 MHz bandwidth, 1 stokes, 2 minute integration
              mask = '/import/extreme2/azic/phd/GMRT_30_070/CASA/final/TVLM513-46_15000_natural.mask',
              interactive = False,
              iter_num = iter_num,
              timerange = timerange)
        

        print("""
        IMAGING ON %s COMPLETED

        BEGINNING IMAGING ON %s
        """ %(split_name, msname))
        
        #image using original dataset
        image('TVLM513-46',
              msname,
              casadir,
              10000,
              '1mJy',
              mask = '/import/extreme2/azic/phd/GMRT_30_070/CASA/final/TVLM513-46_15000_natural.mask',
              interactive = False,
              iter_num = iter_num,
              timerange = timerange)
        
        
        Image_Start_Time = Image_End_Time #increment image start time
        iter_num += 1
