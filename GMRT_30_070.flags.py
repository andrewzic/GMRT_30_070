
def apply_manual_flags(msname):

    """apply manual flags to data. msname is abs path to ms file
    """

    flagmanager(vis = msname, mode = 'save', versionname = 'ORIGINAL_DATA')
    
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C14')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W01') #these antennas were down. see obs log
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W03')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'S06')

    flagdata(vis = msname, mode = 'manual', flagbackup = True, uvrange='0~3.0klambda') #flag short baselines.

    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:0~5')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:23~25')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:57~100')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:119~121')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:134~136')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:148')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:183~185')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:207')
#    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:254')
    
    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:245~255') #the last few channels have phase errors after calibration.

    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C02&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C03&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C04&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C05&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C06&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C08&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C10&W02')

    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&E02')
    #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&E05')
    #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&E06')
    #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&E05')
    #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&W04')
    #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&W05')
    #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&W06')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C02&E05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C02&E04')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C03&C08')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C04&C05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C04&C08')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C04&C13')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C05&C08')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C06&C09')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C06&C13')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C08&W05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C09&C13')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C09&E05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C09&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C10&S02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C10&W05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C11&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C12&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C13&S01')

    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&E03')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&E04')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&E05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&E06')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&S02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E03&E04')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E03&E05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E03&E06')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E03&W05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E04&E05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E04&E06')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E04&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E05&E06')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E05&W02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E05&W04')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E05&W06')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E06&S04')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E06&W06')

    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'S01&S02')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'S03&S04')

    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W02&W04')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W02&W05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W02&W06')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W03&W05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W04&W05')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W04&W06')
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W05&W06')


msname = '30_070_25SEP2016.LTA_RRLL.RRLLFITS.ms'
apply_manual_flags(msname)
