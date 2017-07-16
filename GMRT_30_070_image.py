import os
import shutil
import time
from astropy.time import Time, TimeDelta
import astropy.units as u
import math

execfile('/import/extreme2/azic/phd/GMRT_30_070/GMRT_pipeline_azic.py')
execfile('/import/extreme2/azic/phd/GMRT_30_070/GMRT_30_070_casa_setup.py')
casadir = '/import/extreme2/azic/phd/GMRT_30_070/CASA/10072017_171849/'

#now image each field
'''
for s_key in field_dict:
    
    s_name = field_dict[s_key]
    
    if s_name == 'TVLM513-46':
        threshold = '%fmJy' %clean_threshold_target
        usescratch = True
    else:
        threshold = '%fmJy' %clean_threshold_cal
        usescratch = False
        continue
        
    image(s_name,
          msname,
          casadir,
          15000,
          threshold,
          interactive = True,
          mask = '/import/extreme2/azic/phd/GMRT_30_070/CASA/final/TVLM513-46_15000_natural.mask',
          usescratch = True,
          im_size = [4096, 4096],
          cell_size = 0.51,
          stokes = 'I',
          weighting = 'natural')

if os.path.exists(casadir + '30_070_uvsub.ms'):
    shutil.rmtree(casadir+ '30_070_uvsub.ms')
shutil.copytree(msname, casadir+'30_070_uvsub.ms')
print('doing uvsub')
uvsub(casadir + '30_070_uvsub.ms')

threshold = '0.08mJy' #clean a bit deeper than the 0.1 mJy used w/o uv sub
image(s_name,
      casadir + '30_070_uvsub.ms',
      casadir,
      15000,
      threshold,
      interactive = False,
      mask = '/import/extreme2/azic/phd/GMRT_30_070/CASA/10072017_171849/30_070_25SEP2016.LTA_RRLL.RRLLFITS_TVLM513-46_niter15000_thresh0.100000mJy_natural.mask/',
      usescratch = False,
      im_size = [4096, 4096],
      cell_size = 0.51,
      stokes = 'I',
      weighting = 'natural')
'''
timebins = [8.0*int_time, 19.0*int_time, 37.0*int_time]
thresholds = [2.0*0.588, 2.0*0.37, 2.0*0.26] 

fine_timebins = [2.0*int_time, 3.0*int_time, 4.0*int_time, 6.0*int_time]
fine_thresholds = [2.0*1.14, 2.0*0.92, 2.0*0.8, 2.0*0.66]

# Final_Times_jd = Time([2457657.03844, 2457657.03714, 2457657.03341]) #start jd's for image snapshots for run ending at 12:56:00
# Start_Times_jd = Final_Times_jd + TimeDelta(timebins*u.s)
# start_times = [i.replace('2016-09-25 ', '') for i in Start_Times_jd.iso]
 
#timebin = 8.0*int_time #128.8488 sec, average over exactly 8 integrations
#threshold = 2.0*0.588 mJy #clean thresh in mJy for 2 minutes
#timebin = 19.0*int_time #306.0159 sec, average over exactly 19 integrations
#threshold = 2.0*0.37 mJy #clean thresh in mJy for 5 minutes
#timebin = 37.0*int_time #595.9257 sec, average over 37 integrations
#threshold = 2.0*0.26 #clean thresh in mJy for 21MHz bw, 23 live antennas, 1 stokes for 10 minutes

#clean(vis = msname, selectdata = True, field = 'TVLM513-46', 


split_msnames = []

for timebin, threshold in zip(fine_timebins, fine_thresholds): #doing higher time resolution imaging
    
    Image_Duration = TimeDelta(timebin*u.s) #image duration as astropy.time.Time object

    for i in range(9):
        
        scan = str(3+2*i) #all odd scans up till 19 starting from 3
    
        print("""
PROCESSING SCAN %i
        """ %int(scan))
        
        uvsub_msname = casadir + '30_070_uvsub.ms'
        #    split_name = split_msname('30_070_uvsub.ms',
        #                              scan = scan,
        #                              timebin = '%fs' %timebin,
        #                              width = 256) #returns name of split ms file
        
        #    split_msnames.append(split_name)
        #    print split_name
        
    
        start_time = scan_start_times[scan] #start time of scan
        end_time = scan_end_times[scan] #end time of scan
        
        Start_Time = Time('%s %s' %(obs_date, start_time)) #start time of scan as astropy.time.Time object
        Image_Start_Time = Time('%s %s' %(obs_date, start_time)) #likewise for start time of image, initialise to Start_Time
        End_Time = Time('%s %s' %(obs_date, end_time)) #likewise for end time of scan
        
        Scan_Duration = End_Time - Start_Time
        
        
        #Final_Time = Time('%s 12:56:00' %obs_date) #we only want to image up till here
        
        numchunks = int(math.ceil(Scan_Duration/Image_Duration))
        
        print("""
BEGINNING IMAGING IN TIME CHUNKS OF %f SECONDS
        """ %timebin)
    
        iter_num = 0
        break_flag = False
        while Image_Start_Time < End_Time:
                
         #   if Image_Start_Time >= Final_Time:
         #       break_flag = True
         #       break

            Image_Start_Time_jd = float(Image_Start_Time.jd) #start time of image in julian day
        
            Image_Start_Time_dt = Image_Start_Time.datetime #datetime format
            image_start_time = '%.2i:%.2i:%04.1f' %(Image_Start_Time_dt.hour, Image_Start_Time_dt.minute, float(Image_Start_Time_dt.second) + Image_Start_Time_dt.microsecond*1.0E-6) #convert into CASA-friendly format
        
            Image_End_Time = Image_Start_Time + Image_Duration #end time of image
        
            Image_End_Time_dt = Image_End_Time.datetime #datetime format
            image_end_time = '%.2i:%.2i:%04.1f' %(Image_End_Time_dt.hour, Image_End_Time_dt.minute, float(Image_End_Time_dt.second) + Image_End_Time_dt.microsecond*1.0E-6) #convert image end time to CASA-friendly format

            timerange = '%s~%s' %(image_start_time, image_end_time) #finally give the timerange as casa is expecting it
        
            print("""
TIMERANGE %s
BEGGINING IMAGING ON %s
CHUNK %i of %i
            """ %(timerange, uvsub_msname, iter_num, numchunks))
            #image using uvsub image
            image('TVLM513-46',
                  uvsub_msname,
                  casadir,
                  10000,
                  threshold,
                  mask = '/import/extreme2/azic/phd/GMRT_30_070/CASA/10072017_171849/30_070_25SEP2016.LTA_RRLL.RRLLFITS_TVLM513-46_niter15000_thresh0.100000mJy_natural.mask/',
                  interactive = False,
                  scan = scan,
                  im_size = [2048,2048],
                  timerange = timerange,
                  image_jd = Image_Start_Time_jd,
                  image_duration = timebin,
                  start_freq = start_freq,
                  width = None)
        
            print("""
IMAGING ON UVSUB DATA COMPLETE
            """)        
        
            print("""
TIMERANGE: %s
BEGINNING IMAGING ON %s
CHUNK %i of %i
            """ %(timerange, msname, iter_num, numchunks))
        
            #image using original dataset
            image('TVLM513-46',
                  msname,
                  casadir,
                  10000,
                  threshold,
                  mask = '/import/extreme2/azic/phd/GMRT_30_070/CASA/10072017_171849/30_070_25SEP2016.LTA_RRLL.RRLLFITS_TVLM513-46_niter15000_thresh0.100000mJy_natural.mask/',
                  interactive = False,
                  im_size = [2048, 2048],
                  scan = scan,
                  timerange = timerange,
                  image_jd = Image_Start_Time_jd,
                  image_duration = timebin,
                  start_freq = start_freq,
                  width = None)
        
            Image_Start_Time = Image_End_Time #increment image start time
            iter_num += 1
        
        if break_flag: #have finished imaging the required amount of data
            break
            
