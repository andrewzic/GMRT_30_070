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
    
    ant_flag_str = 'C14'
    ant_flag_str += ',W01' #these first two antennas were down, see observing log
    ant_flag_str += ',W03'
    ant_flag_str += ',S06'
    ant_flag_str += ',E05' #phase errors in secondary cal
    ant_flag_str += ',E06' #amp and phase errors in secondary cal
    ant_flag_str += ',W06' #phase errors in secondary cal

    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = ant_flag_str)
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C14')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W01') #these antennas were down. see obs log
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W03')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'S06')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E05') #phase errors in secondary cal
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E06') #amplitude and phase errors in primary cal
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W06') #bad when calibration solutions are applied to secondary calibrator



    flagdata(vis = msname, mode = 'manual', flagbackup = True, uvrange='0~3.0klambda') #flag short baselines.
    
    channel_flag_str = '0:0~7'
    channel_flag_str += ';23~25'
    channel_flag_str += ';57~100'
    channel_flag_str += ';119~121'
    channel_flag_str += ';134~136'
    channel_flag_str += ';148'
    channel_flag_str += ';183~185'
    channel_flag_str += ';207'
    channel_flag_str += ';244~255'
    
    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = channel_flag_str)
    
#     flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:0~7')
#     flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:23~25')
#     flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:57~100')
#     flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:119~121')
#     flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:134~136')
#     flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:148')
#     flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:183~185')
#     flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:207')
# #    flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:254')
    
#     flagdata(vis = msname, mode = 'manual', flagbackup = True, spw = '0:244~255') #the last few channels have phase errors after calibration.

    #W05;!S03;!W04;!E02;!C13;!W05; !E04!C00&W05;!C01&W05;!C02&W05; !S04&W05; !C03&E04; !C06&E04; !C08&E04; !C09&E04; !C11&E04; !C12&E04


    baseline_flag_str = 'C00&W02'
#    baseline_flag_str += ';C00&E05'
#    baseline_flag_str += ';C00&E06'
#    baseline_flag_str += ';C00&W04'
#    baseline_flag_str += ';C00&W05'
#    baseline_flag_str += ';C00&W06'
    baseline_flag_str += ';C02&W02'
    baseline_flag_str += ';C03&W02'
    baseline_flag_str += ';C04&W02'
    baseline_flag_str += ';C05&W02'
    baseline_flag_str += ';C06&W02'
    baseline_flag_str += ';C08&W02'
    baseline_flag_str += ';C09&W02'
    baseline_flag_str += ';C10&W02'
    baseline_flag_str += ';C11&W02'
    baseline_flag_str += ';C12&W02'

    baseline_flag_str += ';C00&C03'
    baseline_flag_str += ';C00&E02'
    baseline_flag_str += ';C00&W05'
    baseline_flag_str += ';C01&C03'
    baseline_flag_str += ';C01&C04'
    baseline_flag_str += ';C01&E02'
    baseline_flag_str += ';C01&S03'
    baseline_flag_str += ';C01&W05'
    baseline_flag_str += ';C02&E05'
    baseline_flag_str += ';C02&E04'
    baseline_flag_str += ';C02&S03'
    baseline_flag_str += ';C02&W05'
    baseline_flag_str += ';C03&C08'
    baseline_flag_str += ';C03&C10'
    baseline_flag_str += ';C03&C12'
    baseline_flag_str += ';C03&E02'
    baseline_flag_str += ';C03&E04'
    baseline_flag_str += ';C04&C05'
    baseline_flag_str += ';C04&C08'
    baseline_flag_str += ';C04&C13'
    baseline_flag_str += ';C05&C08'
    baseline_flag_str += ';C05&C11'
    baseline_flag_str += ';C06&C09'
    baseline_flag_str += ';C06&C13'
    baseline_flag_str += ';C09&E04'
    baseline_flag_str += ';C09&E05'
    baseline_flag_str += ';C10&E02'
    baseline_flag_str += ';C10&S02'
    baseline_flag_str += ';C10&W05'
    baseline_flag_str += ';C11&E02'
    baseline_flag_str += ';C11&E04'
    baseline_flag_str += ';C11&C12'
    baseline_flag_str += ';C11&C13'
    baseline_flag_str += ';C12&E04'
    baseline_flag_str += ';C13&E04'
    baseline_flag_str += ';C13&S01'

    baseline_flag_str += ';E02&E03'
    baseline_flag_str += ';E02&E04'
    baseline_flag_str += ';E02&E05'
    baseline_flag_str += ';E02&E06'
    baseline_flag_str += ';E02&W02'
    baseline_flag_str += ';E02&W05'
    baseline_flag_str += ';E02&S02'
    baseline_flag_str += ';E03&E04'
    baseline_flag_str += ';E03&E05'
    baseline_flag_str += ';E03&E06'
    baseline_flag_str += ';E03&W04'
    baseline_flag_str += ';E03&W05'
    baseline_flag_str += ';E04&E05'
    baseline_flag_str += ';E04&E06'
    baseline_flag_str += ';E04&W02'
    baseline_flag_str += ';E04&W04'
    baseline_flag_str += ';E04&W05'
#    baseline_flag_str += ';E05&E06'
#    baseline_flag_str += ';E05&W02'
#    baseline_flag_str += ';E05&W04'
#    baseline_flag_str += ';E05&W06'
    baseline_flag_str += ';E06&S04'
#    baseline_flag_str += ';E06&W06'

    baseline_flag_str += ';S01&S02'
    baseline_flag_str += ';S03&S04'
    baseline_flag_str += ';S04&W05'

    baseline_flag_str += ';W02&W04'
    baseline_flag_str += ';W02&W05'
    #    baseline_flag_str += ';W02&W06'
    baseline_flag_str += ';W03&W05'
    baseline_flag_str += ';W04&W05'
    #    baseline_flag_str += ';W04&W06'
    #    baseline_flag_str += ';W05&W06'

    flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = baseline_flag_str)




    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C02&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C03&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C04&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C05&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C06&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C08&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C10&W02')

    

    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&C03')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&E02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&W05')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&E06')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&E05')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&W04')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&W05')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C00&W06')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C01&C03')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C01&C04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C01&E02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C01&S03')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C01&W05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C02&E05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C02&E04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C02&S03')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C02&W05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C03&C08')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C03&C10')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C03&C12')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C03&E02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C03&E04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C04&C05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C04&C08')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C04&C13')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C05&C08')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C05&C11')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C06&C09')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C06&C13')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C06&E02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C06&E04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C08&E04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C08&W05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C09&C13')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C09&E04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C09&E05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C09&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C10&E02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C10&S02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C10&W05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C11&E02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C11&E04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C11&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C11&C12')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C11&C13')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C12&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C12&E04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C13&E04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'C13&S01')

    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&E03')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&E04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&E05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&E06')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&W04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&W05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E02&S02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E03&E04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E03&E05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E03&E06')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E03&W04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E03&W05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E04&E05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E04&E06')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E04&W02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E04&W04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E04&W05')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E05&E06')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E05&W02')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E05&W04')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E05&W06')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E06&S04')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'E06&W06')

    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'S01&S02')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'S03&S04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'S04&W05')

    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W02&W04')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W02&W05')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W02&W06')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W03&W05')
    # flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W04&W05')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W04&W06')
    # #flagdata(vis = msname, mode = 'manual', flagbackup = True, antenna = 'W05&W06')



msname = '30_070_25SEP2016.LTA_RRLL.RRLLFITS.ms'
apply_manual_flags(msname)
