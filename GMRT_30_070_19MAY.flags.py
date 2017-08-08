def flag_stats(msname, note = ''):
    default('flagdata')
    t = flagdata(vis = msname, mode='summary', field='', action='calculate')
    print('FLAG STATISTICS (%s)' %note)
    print('\nAntenna, ')
    for k in sorted(t['antenna']):
        print(k +': %.2f%% - ' % (100.*t['antenna'][k]['flagged']/t['antenna'][k]['total']))
    print('\nCorrelation, ')
    for k, v in t['correlation'].items():
        print(k +': %.2f%% - ' % (100.*v['flagged']/v['total']))
    print('\nSpw, ')
    for k, v in t['spw'].items():
        print(k +': %.2f%% - ' % (100.*v['flagged']/v['total']))
    print('\nTotal: %.2f%%' % (100.*t['flagged']/t['total']))


def apply_manual_flags(msname):

    """apply manual flags to data. msname is abs path to ms file
    """

    flagmanager(vis = msname, mode = 'save', versionname = 'ORIGINAL_DATA')
    """
    32. Name of Non-Working Antennas (with reason for each) :
    C06 : : No Fringe.
    E05 : : Reflector surface refurbishment.
    """
    
    ant_flag_str = 'C06' #no fringe
    ant_flag_str += ',E05' #reflector surface refurbishment
    #ant_flag_str += ',W01' #bad data in bandpass
    ant_flag_str += ',E06' #bad phase solutions for bandpass calibration
    ant_flag_str += ',S04' #worse phase solutions for bp
    ant_flag_str += ',S06' #even worse phase solutions for bp
    ant_flag_str += ',C05' #bad phase solutions with frequency dependent gain calibration
    ant_flag_str += ',C00' #looks bad after applying calibrations

    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = ant_flag_str)

    """
    19:20 : S04 - servo applied stow due to high wind indication.
    19:29 : S04 servo released stow and started working.
    """
    #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'S04', timerange = '19:20:00~19:29:00') #wind hold for this antenna
    
    flagdata(vis = msname, mode = 'manual', flagbackup = True, uvrange='0~5.0klambda') #flag short baselines.
    
    channel_flag_str = '0:0'
    channel_flag_str += ';23~25'
    channel_flag_str += ';57~100'
    channel_flag_str += ';120'
    channel_flag_str += ';135~136'
    channel_flag_str += ';171~175'
    channel_flag_str += ';184~200'
    channel_flag_str += ';207'
    channel_flag_str += ';250~255' #bad phases in primary cal
    
    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = channel_flag_str)
    
    timerange_flag_str = '17:22:00~17:24:50' #first bit of scan
    flagdata(vis = msname, mode = 'manual', flagbackup = True, timerange = timerange_flag_str)
    
    #baselines showing spurious amplitude spikes at some times
    baseline_flag_str = 'C00&E03'
    baseline_flag_str += ';E02&E03'
    baseline_flag_str += ';S02&S03'
    baseline_flag_str += ';S03&S04'
    baseline_flag_str += ';C09&S01'
    baseline_flag_str += ';C03&C13'
    baseline_flag_str += ';C09&C13'
    baseline_flag_str += ';C11&S01'
    baseline_flag_str += ';C01&E03'
    baseline_flag_str += ';C10&E03'
    baseline_flag_str += ';C14&E03'
    
    #baselines showing spurious amplitude in uvwave vs amp for primary cal after full calibration
    baseline_flag_str += ';C11&E04'
    baseline_flag_str += ';E03&E04'
    baseline_flag_str += ';E02&E04'
    baseline_flag_str += ';C00&E04'
    baseline_flag_Str += ';E04&W04'
    
    baseline_flag_str += ';E04&W01' #bad amp in bandpass

    baseline_flag_str += ';C00&E02' #bad amp in phase cal after initial bp'

    #bad phases in primary cal after full calibration
    baseline_flag_str += ';C01&E04'
    baseline_flag_str += ';C04&E04'
    
    '''
    baseline_flag_str += ';E04&S01'
    baseline_flag_str += ';E04&S02'
    baseline_flag_str += ';S01&S03'
    baseline_flag_str += ';C11&W03'
    baseline_flag_str += ';S03&W05'
    baseline_flag_str += ';S03&W06'
    baseline_flag_str += ';C08&S02'
    upon talking to christene, mostly not too bad - only a couple of degrees out - if more than 10 or 20 degrees then worry.
    '''
    
    baseline_flag_str += ';C13&W01'

    #bad baselines in some scans in phase cal after full cal
    baseline_flag_str += ';W03&W06' 
    baseline_flag_str += ';C00&W06'
    baseline_flag_str += ';C00&W03'
    baseline_flag_str += ';C08&W03'
    baseline_flag_str += ';C00&W05'
    baseline_flag_str += ';E04&W03'
    baseline_flag_str += ';W03&W04'
    baseline_flag_str += ';C00&C11'
    baseline_flag_str += ';C08&W06'
    baseline_flag_str += ';C08&E04'
    baseline_flag_str += ';C00&W02'
    baseline_flag_str += ';W05&W06'
    baseline_flag_str += ';C08&W05'
    baseline_flag_str += ';C00&W04'
    baseline_flag_str += ';C11&W06'
    baseline_flag_str += ';E04&W06'
    baseline_flag_str += ';W04&W05'
    baseline_flag_str += ';W02&W06'
    baseline_flag_str += ';W03&W05'
    baseline_flag_str += ';C08&W02'
    baseline_flag_str += ';W04&W06'
    baseline_flag_str += ';W02&W03'
    baseline_flag_str += ';W02&W04'
    baseline_flag_str += ';W02&W05'
    baseline_flag_str += ';E04&S03'

    
    #bad phases in primary cal:
    baseline_flag_str += ';C10&E04'
    baseline_flag_str += ';C11&W02'
    
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = baseline_flag_str)
    
    #other primary cal phase errors
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'S02&W05', spw = '0:5') #S02&W05 phase error in chan 5
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W06', spw = '0:3') #W06 phase error chan 3

    """
    dealing with bad data from antenna W01
    """

    antenna_flag_str = 'W01'
    channel_flag_str = '0:167~176'
    channel_flag_str += ';183~211'
    channel_flag_str += ';53~56'
    channel_flag_str += ';240~255'
    channel_flag_str += ';3~5'
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = antenna_flag_str, spw = channel_flag_str)
    
    '''
    #flagging one bad baseline showing bad amplitude in phase cal amp vs channel after initial bandpass cal
    baseline_flag_str = 'C00&E02'
    timerange_flag_str = '12:56:00~12:57:00'
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = baseline_flag_str, timerange = timerange_flag_str)
    
    #bad baselines at particular scans in phase cal after full bandpass, gain and flux calibration
    baseline_flag_str = 'W03&W06'
    scan_flag_str = '12~16'
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = baseline_flag_str, scan = scan_flag_str)
    
    baseline_flag_str = 'C00&W06'
    scan_flag_str = '12~16'
    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = baseline_flag_str, scan = scan_flag_str)
    '''
#msname = '/import/extreme2/azic/GMRT_30_070/19may/30_070_19MAY2016_16S.LTA_RRLL.RRLLFITS.ms'
apply_manual_flags(msname)
