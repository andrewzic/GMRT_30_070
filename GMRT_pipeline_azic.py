import os
import glob
import shutil
import datetime
import numpy as np

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


def flagcal(caltable, sigma = 5, cycles = 3):
    """from christene's pipeline """
    
    tb.open(caltable, nomodify=False)
    if 'CPARAM' in tb.colnames():
        pars=tb.getcol('CPARAM')
    elif 'FPARAM' in tb.colnames():
        pars=tb.getcol('FPARAM')
    else:
        print("Cannot flag "+caltable+". Unknown type.")
        return False
        
    flags=tb.getcol('FLAG')
    ants=tb.getcol('ANTENNA1')
    totflag_before = sum(flags.flatten())
    
    for c in xrange(cycles):
        for ant in set(ants):
            parant = pars[:,:, np.where( ants == ant ) ]
            flagant = flags[:,:, np.where( ants == ant ) ]
            good = np.logical_not(flagant)
            if sum(good.flatten()) == 0: continue # all flagged antenna, continue
            flagant[ np.abs( parant - np.mean(parant[good]) ) > sigma * np.std( parant[good] ) ] = True
            flags[:,:, np.where( ants == ant ) ] = flagant

    tb.putcol('FLAG', flags)
    totflag_after = sum(flags.flatten())
    print(caltable+": Flagged "+str(totflag_after-totflag_before)+" points out of "+str(len(flags.flatten()))+".")
    
    tb.close()
    return True





def plot_gaincal(caltable, amp = False, phase = False, baseline = False, delay = False, plotdir  = '/import/extreme2/azic/phd/GMRT_30_070/CASA/plots/'):
    
    """
    make useful summary plots for gain calibration solutions
    """
    table_loc = casac.table()
    table_loc.open( '%s/ANTENNA' %caltable)
    antenna_name = table_loc.getcol('NAME')
    antenna_num = len(antenna_name)
    table_loc.close()
    
    nplots = int(antenna_num/3)
    
    if amp:
        for i in range(nplots):
            plot_file = '%s%samp_time_%i.png' %(plotdir, os.path.basename(caltable), i)
            if os.path.exists(plot_file):
                os.remove(plot_file)
            ant_plot = '%i~%i' %(i*3, i*3+2)
            if baseline:
                xaxis = 'antenna2'
                plotsymbol = 'o'
            else:
                xaxis = 'time'
                plotsymbol = 'o-'
                
            default('plotcal')
            plotcal(caltable = caltable,
                    xaxis = xaxis,
                    yaxis = 'amp',
                    antenna = ant_plot,
                    subplot = 311,
                    iteration = 'antenna',
                    plotsymbol = plotsymbol,
                    plotcolor = 'red',
                    markersize = 5.0,
                    fontsize = 10.0,
                    showgui = False,
                    figfile = plot_file)
            
    if phase:
        for i in range(nplots):
            plot_file = '%s%sphase_time_%i.png' %(plotdir, os.path.basename(caltable), i)
            if os.path.exists(plot_file):
                os.remove(plot_file)
            ant_plot = '%i~%i' %(3*i, 3*i+2)
            if baseline:
                xaxis = 'antenna2'
            else:
                xaxis = 'time'

            default('plotcal')
            plotcal(caltable = caltable,
                    xaxis = xaxis,
                    yaxis = 'phase',
                    antenna = ant_plot,
                    subplot = 311,
                    overplot = False,
                    clearpanel = 'Auto',
                    iteration = 'antenna',
                    plotrange = [0, 0, -180, 180],
                    plotsymbol = 'o-',
                    plotcolor = 'blue',
                    markersize = 5.0,
                    fontsize = 10.0, 
                    showgui = False,
                    figfile = plot_file)

            xaxis = 'chan'
            plot_file = '%s%sphase_chan_%i.png' %(plotdir, os.path.basename(caltable), i)

            plotcal(caltable = caltable,
                    xaxis = xaxis,
                    yaxis = 'phase',
                    antenna = ant_plot,
                    subplot = 311,
                    overplot = False,
                    clearpanel = 'Auto',
                    iteration = 'antenna',
                    plotrange = [0, 0, -180, 180],
                    plotsymbol = 'o-',
                    plotcolor = 'blue',
                    markersize = 5.0,
                    fontsize = 10.0, 
                    showgui = False,
                    figfile = plot_file)
            
    if delay:
        for i in range(nplots):
            plot_file = '%s%sdelay_%i.png' %(plotdir, os.path.basename(caltable), i)
            if os.path.exists(plot_file):
                os.remove(plot_file)
            ant_plot = '%i~%i' %(3*i, 3*i+2)
            
            default('plotcal')
            plotcal(caltable = caltable,
                    xaxis = 'time',
                    yaxis = 'delay',
                    antenna = ant_plot,
                    subplot = 311,
                    overplot = False,
                    clearpanel = 'Auto',
                    iteration = 'antenna',
                    plotrange = [],
                    plotsymbol = 'o-',
                    markersize = 5.0,
                    fontsize = 10.0,
                    showgui = False,
                    figfile = plot_file)


    return True
                    
def plot_bandpass(caltable, amp = False, phase = False, plotdir = '/import/extreme2/azic/phd/GMRT_30_070/CASA/plots/'):
    
    """
    make useful summary plots for bandpass calibration solutions
    """
    
    tb.open(caltable)
    data_var_col = tb.getvarcol('CPARAM')
    flag_var_col = tb.getvarcol('FLAG')
    tb.close()
    
    rowlist = data_var_col.keys()
    nrows = len(rowlist)
    for row in rowlist:
        data_array = data_var_col[row]
        flag_array = flag_var_col[row]
        amps = np.abs(data_array)
        phases = np.arctan2(np.imag(data_array), np.real(data_array))
        unflagged = np.logical_not(flag_array)
        temp_array = amps[unflagged]
        
        max_amp = 0.0
        max_phase = 0.0
        
        if len(temp_array) > 0:
            max_amp_tmp = np.amax(temp_array)
            if max_amp_tmp > max_amp:
                max_amp = max_amp_tmp
        
        temp_array = np.abs(phases[unflagged])
        
        if len(temp_array) > 0:
            max_phase_tmp = np.amax(temp_array)*180.0/np.pi
            if max_phase_tmp > max_phase:
                max_phase = max_phase_tmp
        
    table_loc = casac.table()
    table_loc.open('%s/ANTENNA' %caltable)
    antenna_name = table_loc.getcol('NAME')
    antenna_num = len(antenna_name)
    table_loc.close()
    
    nplots = int(antenna_num/3)
    
    if amp:
        yaxis = 'amp'
        ymin = '0'
        ymax = 1.1*max_amp
        for i in range(nplots):
            file_name = '%s%s_amp_%i.png' %(plotdir, os.path.basename(caltable), i)
            if os.path.exists(file_name):
                os.remove(file_name)
            ant_plot = '%i~%i' %(3*i, 3*i+2)
            default('plotcal')
            plotcal(caltable = caltable,
                    xaxis = 'freq',
                    yaxis = yaxis,
                    antenna = ant_plot,
                    iteration = 'antenna',
                    subplot = 311,
                    plotrange = [0, 0, ymin, ymax],
                    showflags = False,
                    plotsymbol = 'o',
                    plotcolor = 'blue',
                    markersize = 5.0,
                    fontsize = 10.0,
                    showgui = False,
                    figfile = file_name)
    if phase:
        yaxis = 'phase'
        ymin = -min(185, 1.1*max_phase)
        ymax = min(185, 1.1*max_phase)
        for i in range(nplots):
            
            file_name = '%s%s_phase_%i.png' %(plotdir, os.path.basename(caltable), i)
            if os.path.exists(file_name):
                os.remove(file_name)
            
            ant_plot = '%i~%i' %(3*i, 3*i+2)
            default('plotcal')
            plotcal(caltable = caltable,
                    xaxis = 'freq',
                    yaxis = yaxis,
                    antenna = ant_plot,
                    iteration = 'antenna',
                    subplot = 311,
                    plotrange = [0, 0, ymin, ymax],
                    showflags = False,
                    plotsymbol = 'o',
                    plotcolor = 'blue',
                    markersize = 5.0,
                    fontsize = 10.0,
                    showgui = False,
                    figfile = file_name)

    return True




def import_data(datafile, flagfile, msname):
    
    """
    import the GMRT data into CASA-readable ms file
    """
    
    #import the data with importgmrt
    default('importgmrt') 
    importgmrt(fitsfile = datafile, flagfile = flagfile, vis = msname)
    
    #save the obs info to a text file
    default('listobs')
    listobs(vis = msname, verbose = True, listfile = 'listobs.txt', overwrite = True)

    default('plotants')
    plotants(vis = msname, figfile = 'plots/plotants.png')
    return True



def initial_flagging(msname):
    """
    perform basic initial flagging: quack, clip zeros
    """
    
    default('flagdata')
    flagdata(vis = msname, mode = 'quack', quackinterval = 1, quackmode = 'beg', action = 'apply', flagbackup = False)
    
    default('flagdata')
    flagdata(vis = msname, mode = 'clip', clipzeros = True, correlation = 'ABS_ALL', action = 'apply', flagbackup = False)
    
    default('flagmanager')
    flagmanager(vis = msname, mode = 'save', versionname = 'after_initial_flag', comment = str(datetime.datetime.now()))
    return True



def manual_flagging(msname, manual_flags):
    """
    flag data according to manual flags stored in manual_flags file
    """
    execfile(manual_flags)
    return True


def auto_tf_flagging(msname):
    """
    perform automatic flagging using time-frequency cropping algorithm
    """
    default('flagdata')
    flagdata(vis = msname, mode = 'tfcrop')
    return True


def auto_r_flagging(msname):
    """
    perform automatic flagging using rflag algorithm
    """
    default('flagdata')
    flagdata(vis = msname, mode = 'rflag', ntime = 'scan', combinescans = False, datacolumn = 'corrected', winsize = 3, timedevscale = 5, freqdevscale = 5, action = 'apply', flagbackup = True)
    return True
    

def init_setjy(msname, flux_cal_name):
    """
    perform initial flux density scaling
    """
    default('setjy')
    setjy_res = setjy(vis = msname, field = flux_cal_name, standard = 'Perley-Butler 2013', scalebychan = True, usescratch = True)
    return setjy_res

def init_bandpass(msname, minsnr, flux_cal_name, refant, caldir, iter_num):
    
    """
    perform initial bandpass calibration. steps:
    1) initial phase calibration on flux calibrator used for bandpass cal
    2) initial bandpass calibration using flux calibrator, taking solutions from phase cal in step 1
    
    """
    spw = '0:150~174'
    
    for step in ['cycle1', 'final']:
        gaintables = []
        interp = []
        
        gaincal_name = '%s%s_bandpass_gainphase_%i_%s.Gp' %(caldir, flux_cal_name, iter_num, step)
        
        default('gaincal')
        gaincal(vis = msname,
                caltable = gaincal_name,
                field = flux_cal_name,
                refant = refant,
                spw = spw,
                calmode = 'p',
                solint = 'int')
        
        gaincal_name_old = gaincal_name
        gaincal_name = gaincal_name.replace('.Gp', '_smooth.Gp')
        tb.clearlocks()
        default('smoothcal')
        smoothcal(vis = msname,
                  tablein = gaincal_name_old,
                  caltable = gaincal_name)

        plot_gaincal(gaincal_name, amp = True, phase = True, plotdir = caldir)
        
        bandpass_name = '%s%s_bandpass_%i_%s.B0' %(caldir, flux_cal_name, iter_num, step)
        default('bandpass')
        bandpass(vis = msname,
                 caltable = bandpass_name,
                 field = flux_cal_name,
                 solint = 'inf',
                 solnorm = True,
                 minsnr = minsnr,
                 bandtype = 'B',
                 gaintable = [gaincal_name],
                 interp = ['linear'])
        
        flagcal(bandpass_name, sigma = 5, cycles = 3)
        
        plot_bandpass(bandpass_name, amp = True, phase = True, plotdir = caldir)
        
        default('gaincal')
        gaincal_name = '%s%s_bandpass_%i_%s.Gap' %(caldir, flux_cal_name, iter_num, step)
        
        gaincal(vis = msname,
                caltable = gaincal_name,
                field = flux_cal_name,
                selectdata = True,
                solint = 'int',
                refant = refant,
                interp = interp + ['nearest'],
                minsnr = minsnr,
                gaintype = 'G',
                calmode = 'ap',
                gaintable = gaintables + [bandpass_name])
        
        flagcal(gaincal_name, sigma = 5, cycles = 3)
        
        plot_gaincal(gaincal_name, amp = True, phase = True, plotdir = caldir)
        
        gaintables.append(gaincal_name)
        interp.append('linear')
        
        badpass_name_old = bandpass_name
        bandpass_name = '%s%s_bandpass_%i_%s.B1' %(caldir, flux_cal_name, iter_num, step)
        bandpass(vis = msname,
                 caltable = bandpass_name,
                 selectdata = True,
                 field = flux_cal_name,
                 solint = 'inf',
                 combine = 'scan,field',
                 refant = refant,
                 interp = interp,
                 minsnr = minsnr,
                 bandtype = 'B',
                 gaintable = gaintables)
        
        plot_bandpass(bandpass_name, amp = True, phase = True, plotdir = caldir)
        gaintables.append(bandpass_name)
        interp.append('nearest,nearestflag')
        
        default('applycal')
        applycal(vis = msname,
                 selectdata = True,
                 field = flux_cal_name,
                 applymode = 'calflagstrict',
                 calwt = False,
                 flagbackup = True,
                 gaintable = [bandpass_name],
                 interp = ['nearest'])
    return bandpass_name



def final_bandpass(msname, minsnr, flux_cal_name, refant, caldir, iter_num):
    
    spw = '0:150~174'
    
    for step in ['final']:
        gaintables = []
        interp = []
        
        gaincal_name = '%s%s_bandpass_gainphase_%i_%s.Gp' %(caldir, flux_cal_name, iter_num, step)
        
        default('gaincal')
        gaincal(vis = msname,
                caltable = gaincal_name,
                field = flux_cal_name,
                refant = refant,
                spw = spw,
                calmode = 'p',
                solint = 'int')
    
        gaincal_name_old = gaincal_name
        gaincal_name = gaincal_name.replace('.Gp', '_smooth.Gp')
        tb.clearlocks()
        default('smoothcal')
        smoothcal(vis = msname,
                  tablein = gaincal_name_old,
                  caltable = gaincal_name)
    
    
        plot_gaincal(gaincal_name, amp = True, phase = True, plotdir = caldir)
        
        bandpass_name = '%s%s_bandpass_%i_%s.B0' %(caldir, flux_cal_name, iter_num, step)
        default('bandpass')
        bandpass(vis = msname,
                 caltable = bandpass_name,
                 field = flux_cal_name,
                 solint = 'inf',
                 solnorm = True,
                 minsnr = minsnr,
                 bandtype = 'B',
                 gaintable = [gaincal_name],
                 interp = ['linear'])
        
        flagcal(bandpass_name, sigma = 5, cycles = 3)
    
        plot_bandpass(bandpass_name, amp = True, phase = True, plotdir = caldir)
    
        default('gaincal')
        gaincal_name = '%s%s_bandpass_%i_%s.Gap' %(caldir, flux_cal_name, iter_num, step)
        
        gaincal(vis = msname,
                caltable = gaincal_name,
                field = flux_cal_name,
                selectdata = True,
                solint = 'int',
                refant = refant,
                interp = interp + ['nearest'],
                minsnr = minsnr,
                gaintype = 'G',
                calmode = 'ap',
                gaintable = gaintables + [bandpass_name])
    
        flagcal(gaincal_name, sigma = 5, cycles = 3)
        
        plot_gaincal(gaincal_name, amp = True, phase = True, plotdir = caldir)
        
        gaintables.append(gaincal_name)
        interp.append('linear')
        
        badpass_name_old = bandpass_name
        bandpass_name = '%s%s_bandpass_%i_%s.B1' %(caldir, flux_cal_name, iter_num, step)
        bandpass(vis = msname,
                 caltable = bandpass_name,
                 selectdata = True,
                 field = flux_cal_name,
                 solint = 'inf',
                 combine = 'scan,field',
                 refant = refant,
                 interp = interp,
                 minsnr = minsnr,
                 bandtype = 'B',
                 gaintable = gaintables)
             
        plot_bandpass(bandpass_name, amp = True, phase = True, plotdir = caldir)
    return bandpass_name



def final_gaincal(msname, minsnr, field, flux_cal_name, refant, caldir, iter_num, append_bool, bandpass_name):
    
    gaintables = [bandpass_name]
    spw = '0:20~240'
    gaincal_name = '%s%s_gaincal_final.Gap' %(caldir, flux_cal_name)
    gaincal(vis = msname,
            caltable = gaincal_name,
            field = field,
            solint = 'int',
            spw = spw,
            refant = refant,
            calmode = 'ap',
            gaintype = 'G',
            gaintable = gaintables,
            append = append_bool)
    
    flagcal(gaincal_name, sigma = 5, cycles = 3)
    
    gaincal_name_old = gaincal_name
    gaincal_name = gaincal_name.replace('.Gap', '_smooth.Gap')
    tb.clearlocks()
    default('smoothcal')
    smoothcal(vis = msname, tablein = gaincal_name_old, caltable = gaincal_name)
    
    plot_gaincal(gaincal_name, amp = True, phase = True, plotdir = caldir)
    
    return gaincal_name_old



def final_fluxscale(msname, flux_cal_name, other_cals, caldir, gaincal_name):
    
    #flux_cal_name is a list, ['3C286']
    fluxcal_name = '%s%s_fluxcal.Ga_fluxscale' %(caldir, flux_cal_name[0])
    
    default('fluxscale')
    #for s in other_cals:
    fluxscale_res = fluxscale(vis = msname,
                              caltable = gaincal_name,
                              fluxtable = fluxcal_name,
                              reference = flux_cal_name,
                              transfer = other_cals)
    return fluxcal_name
        


def final_applycal(msname, flux_cal_name, gaintables, interps, gainfields):
    
    default('applycal')
    applycal(vis = msname,
             field = flux_cal_name,
             gaintable = gaintables,
             gainfield = gainfields,
             interp = interps,
             applymode = 'calflagstrict',
             calwt = False,
             flagbackup = True)
    return True
                                  

def diagnostic_plotms(msname, caldir, flux_cal_name):
    default('plotms')
    xdatacolumn = 'corrected'
    ydatacolumn = 'corrected'
    showgui = False
    
    correlation = 'RR,LL'
    overwrite = True
    

    coloraxis = 'baseline'
    
    xaxis = 'time'
    yaxis = 'amp'
    field = ''
    plot_file = '%sallfields_amp_time_corrected.png' %(caldir)
    plotms(vis = msname, selectdata = True, xdatacolumn = xdatacolumn, ydatacolumn = ydatacolumn, correlation = correlation, overwrite = overwrite, field = field, xaxis = xaxis, yaxis = yaxis, coloraxis = coloraxis, plotfile = plot_file, showgui = showgui)
    
    field = flux_cal_name
    plot_file = '%s%s_amp_time_corrected.png' %(caldir, flux_cal_name)
    plotms(vis = msname, selectdata = True, xdatacolumn = xdatacolumn, ydatacolumn = ydatacolumn, correlation = correlation, overwrite = overwrite, field = field, xaxis = xaxis, yaxis = yaxis, coloraxis = coloraxis, plotfile = plot_file, showgui = showgui)

    xaxis = 'baseline'
    plot_file = '%s%s_amp_baseline_corrected.png' %(caldir, flux_cal_name)
    plotms(vis = msname, selectdata = True, xdatacolumn = xdatacolumn, ydatacolumn = ydatacolumn, correlation = correlation, overwrite = overwrite, field = field, xaxis = xaxis, yaxis = yaxis, coloraxis = 'channel', plotfile = plot_file, showgui = showgui)
    
    xaxis = 'chan'
    plot_file = '%s%s_amp_chan_corrected.png' %(caldir, flux_cal_name)
    plotms(vis = msname, selectdata = True, xdatacolumn = xdatacolumn, ydatacolumn = ydatacolumn, correlation = correlation, overwrite = overwrite, field = field, xaxis = xaxis, yaxis = yaxis, coloraxis = coloraxis, plotfile = plot_file, showgui = showgui)
    
    xaxis = 'uvwave'
    plot_file = '%s%s_amp_uvwave_corrected.png' %(caldir, flux_cal_name)
    plotms(vis = msname, selectdata = True, xdatacolumn = xdatacolumn, ydatacolumn = ydatacolumn, correlation = correlation, overwrite = overwrite, field = field, xaxis = xaxis, yaxis = yaxis, coloraxis = coloraxis, plotfile = plot_file, showgui = showgui)
    
    yaxis = 'phase'
    plotrange = [0,0,-180,180]
    field = flux_cal_name
    for i in range(30):
        xaxis = 'time'
        antenna = str(i)
        plot_file = '%s%s_phase_time_ant%i_corrected.png' %(caldir, flux_cal_name, i)
        plotms(vis = msname, selectdata = True, xdatacolumn = xdatacolumn, ydatacolumn = ydatacolumn, correlation = correlation, overwrite = overwrite, field = field, xaxis = xaxis, yaxis = yaxis, coloraxis = coloraxis, antenna = antenna, plotfile = plot_file, showgui = showgui, plotrange = plotrange)
        
        xaxis = 'chan'
        plot_file = '%s%s_phase_chan_ant%i_corrected.png' %(caldir, flux_cal_name, i)
        plotms(vis = msname, selectdata = True, xdatacolumn = xdatacolumn, ydatacolumn = ydatacolumn, correlation = correlation, overwrite = overwrite, field = field, xaxis = xaxis, yaxis = yaxis, coloraxis = coloraxis, antenna = antenna, plotfile = plot_file, showgui = showgui, plotrange = plotrange)

        xaxis = 'uvwave'
        plot_file = '%s%s_phase_uvwave_ant%i_corrected.png' %(caldir, flux_cal_name, i)
        plotms(vis = msname, selectdata = True, xdatacolumn = xdatacolumn, ydatacolumn = ydatacolumn, correlation = correlation, overwrite = overwrite, field = field, xaxis = xaxis, yaxis = yaxis, coloraxis = coloraxis, antenna = antenna, plotfile = plot_file, showgui = showgui, plotrange = plotrange)
        

    plotrange = [0,0,0,0]
    antenna = ''
    xaxis = 'amp'
    plot_file = '%s%s_phase_amp_corrected.png' %(caldir, flux_cal_name)
    plotms(vis = msname, selectdata = True, xdatacolumn = xdatacolumn, ydatacolumn = ydatacolumn, correlation = correlation, overwrite = overwrite, field = field, xaxis = xaxis, yaxis = yaxis, coloraxis = coloraxis, plotfile = plot_file, showgui = showgui, plotrange = plotrange)

    xaxis = 'real'
    yaxis = 'imag'
    plot_file = '%s%s_imag_real_corrected.png' %(caldir, flux_cal_name)
    plotms(vis = msname, selectdata = True, xdatacolumn = xdatacolumn, ydatacolumn = ydatacolumn, correlation = correlation, overwrite = overwrite, field = field, xaxis = xaxis, yaxis = yaxis, coloraxis = coloraxis, plotfile = plot_file, showgui = showgui, plotrange = plotrange)
