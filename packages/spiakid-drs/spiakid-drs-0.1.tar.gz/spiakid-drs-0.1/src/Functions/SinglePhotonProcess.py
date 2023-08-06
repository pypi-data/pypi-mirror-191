import numpy as np
import matplotlib.pyplot as plt
import pickle
import Functions.utility as ut
import scipy.signal as sg
from lmfit.models import GaussianModel
import Functions.IQCalibration as IQCal

def GenPulseAverage(res,pulsefolder,savefolder,IQCaldata,pulselaser = 250,
                    dt = 1e-8, NumpulseUnscaled = 80,
                    calibrate_drift = True, t_offset = 0.001,savefig = True):
    
    
    pulsePointNum = round(1/pulselaser/dt)
    Ip_av = np.zeros(pulsePointNum)
    Qp_av = np.zeros(pulsePointNum)
    
    processedpulse = 0

    # Idrifts = []
    # Qdrifts = []

    # calibrate_drift = True
    for i in range(NumpulseUnscaled):
        
        # if i not in usfulseg:
            # continue 
        processedpulse += 1;
        filename = pulsefolder + '//%d.obj' %(i)
        
        f = open(filename,'rb')
        pulsedata = pickle.load(f)
        f.close()
        
        print("i:",i)
        # pulsedata = res.pulseUnscaled[i]
        I0 = res.I0;
        Q0 = res.Q0;
        freq = res.freq;
        
        I,Q,pulsemeasfreq,fsample = ut.CalPulseRaw(pulsedata,IQCaldata,freq,I0,Q0,ispulse = True)
        # t = np.arange(0,len(I))*1e-08
        
        # If,Qf = ut.lowpassfiltering(I,100e6,Q,cutoff = 250e3)
        resfreqindx = np.argmin(np.abs(res.freq-pulsemeasfreq*1e9))
        
        
        if i==0:

            Ip_initial = res.I[resfreqindx]
            Qp_initial = res.Q[resfreqindx]
    
        Ip,Qp,pulseIRaws,pulseQRaws = ut.GenAveragePulse(I,Q,dt = dt,pulsefreq = pulselaser,t_offset = t_offset)
        
        points = int((1/pulselaser/2 - t_offset)/dt)
        
        # Idrifts.append(np.mean(Ip[0:10000]))
        # Qdrifts.append(np.mean(Qp[0:10000]))
        # print(np.mean(Ip[0:10000]))
        # print(np.mean(Qp[0:10000]))
        
        if calibrate_drift:
            Ip = Ip - np.mean(Ip[0:points]) + Ip_initial 
            Qp = Qp - np.mean(Qp[0:points]) + Qp_initial 
        
        
        
        Ip_av = Ip + Ip_av;
        Qp_av = Qp + Qp_av;
        
        
    t_seg = np.arange(0,len(Ip_av))*dt
        

    pulsefreq = pulsedata['freq']

    res.pulseUnscaled = []



    Ip_av = Ip_av/processedpulse;
    Qp_av = Qp_av/processedpulse;

    amp,phase = res.cal_pulse_outside(Ip_av + 1j*Qp_av,pulsedata['freq']*1e9,pulsewidth = 50,fs = 200e3)

    data = {"pulsefreq":pulsefreq,
            'res':res,
            't':t_seg,
            'Ia':Ip_av,
            'Qa':Qp_av,
            'amp':amp,
            'phase':phase,
            't_offset':t_offset,
            'dt':dt}

    f = open(savefolder + '/averagedpulse.obj','wb')
    pickle.dump(data,f)

    f.close()
    
    if savefig == True:

        plt.figure()
        
        points = int((1/pulselaser/2 - t_offset)/dt)
        phase0 = np.mean(phase[0:points])
        amp0 = np.mean(amp[0:points])

        phasedeg = -(phase-phase0);

        phasedeg = np.unwrap(phasedeg)
        damp = -(amp-amp0)
        plt.plot(t_seg*1000-t_offset*1000,phasedeg/np.max(phasedeg),label = 'phase')
        plt.plot(t_seg*1000-t_offset*1000,damp/np.max(phasedeg),label = 'amp')


        plt.xlabel('Time(ms)')
        plt.ylabel('Normalized response')

        plt.legend(fontsize = 15)
        plt.grid()

        plt.savefig(savefolder + '/average pulse phase response-norm.svg',bbox_inches = 'tight')
        plt.savefig(savefolder + '/average pulse phase response-norm.jpg',dpi = 600,bbox_inches = 'tight')
        plt.savefig(savefolder + '/average pulse phase response-norm.eps',bbox_inches = 'tight')
        
        # plt.close()
        plt.figure()

        plt.plot(t_seg*1000-t_offset*1000,phasedeg,label = 'phase')
        plt.plot(t_seg*1000-t_offset*1000,damp,label = 'amp')

        plt.xlabel('Time(ms)')
        plt.ylabel('Response(rad)')

        plt.legend(fontsize = 15)
        plt.grid()

        plt.savefig(savefolder + '/average pulse phase response.svg',bbox_inches = 'tight')
        plt.savefig(savefolder + '/average pulse phase response.jpg',dpi = 600,bbox_inches = 'tight')
        plt.savefig(savefolder + '/average pulse phase response.eps',bbox_inches = 'tight')
        # plt.close()
        
    return data


def GenPulseAverageWithHDF(res,hdfile,savefolder,IQCaldata,
                    calibrate_drift = True, t_offset = 0.001,savefig = True,Format = '.jpg'):
    
    #res: scraps.resonator obj
    
    #hdfile: the hdfile contain the pulse data
    
    #savefolder: directory to save the processed the data
    
    #IQCaldata: IQ Calibration data for the raw pulse data
    
    #calibrate_drift: bool, to remove the drift in the baseline or not. 
    
    #t_offset: to move the trigger time of the pulse. t_offset = 0 means the trigger of the pulse is in the center
        
    #savefig: bool, to produce the plot of the averaged data or not
    
    #load the dataset of the pulse in the hdfile
    pulse = hdfile['pulse']
    
    #the frequency of the trigger of the laser.
    pulselaser = pulse.attrs['laserfreq']
    
    #the data of the pulse is segmented. Load the number of the groups
    NumpulseUnscaled = pulse.attrs['groupnum']
    print(NumpulseUnscaled)
    #load the sample frequency of the data. The usual sample rate is about 100MHz
    dt = 1/pulse.attrs['samplefreq']
    
    #calculate the number of data point in one period of the laser pulse
    pulsePointNum = round(1/pulselaser/dt)
    Ip_av = np.zeros(pulsePointNum)
    Qp_av = np.zeros(pulsePointNum)

    # calibrate_drift = True
    for i in range(NumpulseUnscaled):
        
        #load the raw data of the IQ data, which is numpy.int16 
        pulsedata = pulse['IQ%d'%(i)][...]
        
        #load the voltage gain and the offset of the oscilloscope 
        vgains = pulse['vgains'][...]
        voffsets = pulse['voffsets'][...]

        print("i:",i)
        
        #load the DC offset of the IQ from the res
        I0 = res.I0;
        Q0 = res.Q0;
        freq = res.freq;
        
        #load the readout tone frequency
        pulsefreq = pulse.attrs['measfreq']
        
        #scale the data from the oscillscope
        I = pulsedata[0]*vgains[0] - voffsets[0]
        Q = pulsedata[1]*vgains[1] - voffsets[1]
        
        #calibrate the IQ imbalance from the IQ mixer, i.e. the DC offset, amplitude and phase imbalance
        I,Q = IQCal.IQ_CalNoise(I,Q,pulsefreq/1e9,freq/1e9,I0,Q0,IQCaldata)
        
        resfreqindx = np.argmin(np.abs(res.freq-pulsefreq))
        
        #produce the reference for the I and Q of the pulse
        if i==0:

            Ip_initial = res.I[resfreqindx]
            Qp_initial = res.Q[resfreqindx]
        
        #segment the data by laser frequency
        Ip,Qp,pulseIRaws,pulseQRaws = ut.GenAveragePulse(I,Q,dt = dt,pulsefreq = pulselaser,t_offset = t_offset)
        
        #to remove the DC offset or not
        points = int((1/pulselaser/2 - t_offset)/dt)
        if calibrate_drift:
            Ip = Ip - np.mean(Ip[0:points]) + Ip_initial 
            Qp = Qp - np.mean(Qp[0:points]) + Qp_initial 
        
        #calculate the average of the pulse
        Ip_av = Ip + Ip_av;
        Qp_av = Qp + Qp_av;
        
    
    t_seg = np.arange(0,len(Ip_av))*dt
        
    # res.pulseUnscaled = []

    #generate the IQ of the pulse
    Ip_av = Ip_av/NumpulseUnscaled;
    Qp_av = Qp_av/NumpulseUnscaled;
    
    #calculate the amplitude and phase response of the MKIDs
    amp,phase = res.cal_pulse_outside(Ip_av + 1j*Qp_av,pulsefreq,pulsewidth = 50)

    data = {"pulsefreq":pulsefreq,
            'res':res,
            't':t_seg,
            'Ia':Ip_av,
            'Qa':Qp_av,
            'amp':amp,
            'phase':phase,
            't_offset':t_offset,
            'dt':dt}

    #f = open(savefolder + '/averagedpulse.obj','wb')
    #pickle.dump(data,f)
    #f.close()
    
    #produce the plot of the averaged pulse and amplitude of the detector
    if savefig == True:

        plt.figure(1)
        plt.title('Avedata')
        plt.subplot(1,2,1)
        points = int((1/pulselaser/2 - t_offset)/dt)
        phase0 = np.mean(phase[0:points])
        amp0 = np.mean(amp[0:points])

        phasedeg = -(phase-phase0);

        phasedeg = np.unwrap(phasedeg)
        damp = -(amp-amp0)
        plt.plot(t_seg*1000-t_offset*1000,phasedeg/np.max(phasedeg),label = 'phase')
        plt.plot(t_seg*1000-t_offset*1000,damp/np.max(phasedeg),label = 'amp')


        plt.xlabel('Time(ms)')
        plt.ylabel('Normalized response')

        plt.legend(fontsize = 15)
        plt.grid()

        # plt.savefig(savefolder + '/average pulse phase response-norm.svg',bbox_inches = 'tight')
        # plt.savefig(savefolder + '/average pulse phase response-norm.jpg',dpi = 600,bbox_inches = 'tight')
        # plt.savefig(savefolder + '/average pulse phase response-norm.eps',bbox_inches = 'tight')
        
        # plt.close()
      
        plt.subplot(1,2,2)
        plt.plot(t_seg*1000-t_offset*1000,phasedeg,label = 'phase')
        plt.plot(t_seg*1000-t_offset*1000,damp,label = 'amp')

        plt.xlabel('Time(ms)')
        plt.ylabel('Response(rad)')

        plt.legend(fontsize = 15)
        plt.grid()
        
        plt.savefig(savefolder + '/avedata' + Format ,bbox_inches = 'tight')
   
        # plt.savefig(savefolder + '/average pulse phase response.jpg',dpi = 600,bbox_inches = 'tight')
        # plt.savefig(savefolder + '/average pulse phase response.eps',bbox_inches = 'tight')
        # plt.close()
        
    return data

# hdfile

def GenPSDWithHDF(res,hdfile,savefolder,IQCaldata,binsize = 100,
           pulselaser = 250, NoiseSeglength = None, plotpsd = True,Format = ".jpg"):
    
    #res: scraps.resonator obj
    
    #hdfile: the hdfile contain the pulse data
    
    #savefolder: directory to save the processed the data
    
    #IQCaldata: IQ Calibration data for the raw pulse data
    
    #binsize: the data point of averaging the data
      
    #plotpsd: bool, to produce the plot of the averaged data or not
    
    #NoiseSeglength: the length of the data points to perform fft
    
    In,Qn= ut.CalNoiseHDf(res,hdfile,IQCaldata)
    
    fsample = hdfile['noise'].attrs['samplefreq']
    noisefreq = hdfile['noise'].attrs['measfreq']
    
    pulsePointNum = round(1/pulselaser*fsample);
    
    
    if  NoiseSeglength == None:
        NoiseSeglength = int(pulsePointNum/binsize)

    # In = np.concatenate(noiseIs)
    # Qn = np.concatenate(noiseQs)
    
    t_seg = np.arange(0,len(In))*1/fsample
    
    t_bin,In_bined = ut.AverageArray(t_seg,In,chuncksize = binsize)
    t_bin,Qn_bined = ut.AverageArray(t_seg,Qn,chuncksize = binsize)
    
    #calculate the amplitude and phase of the noise spectrum
    pulse_amp,pulse_phase = res.cal_pulse_outside(In_bined + 1j*Qn_bined,noisefreq,pulsewidth = 50,fs = 1/(t_bin[1]-t_bin[0]))
    #remove the 2*pi change
    pulse_phase = np.unwrap(pulse_phase)
    
    #calculate the noise spectrum with welth method in the amplitude and phase direction. 
    fpsd,pxx = sg.welch(pulse_phase-np.mean(pulse_phase),fs = 1/(t_bin[1]-t_bin[0]),nperseg = NoiseSeglength)
    fpsd,pyy = sg.welch(pulse_amp-np.mean(pulse_amp),fs = 1/(t_bin[1]-t_bin[0]),nperseg = NoiseSeglength)
    data = np.vstack([fpsd,pxx,pyy])
    
    np.savetxt(savefolder + '// psd%d.txt'%(binsize),data.T)
    
    #plot the psd
    if plotpsd == True:
        
        ut.SetDefaultPlotParam()
        plt.figure()
        plt.semilogx(fpsd,pxx,label='phase')
        plt.semilogx(fpsd,pyy,label='amp')
        plt.xlabel("Freq(Hz)")
        plt.ylabel("Psd($rad^2/Hz)$")
        plt.legend()
        plt.savefig(savefolder + "//psd%d.jpg"%(binsize),dpi = 600,bbox_inches = 'tight')
        
    return data.T

def GenPSDFromNoise(res,IQCaldata,savefolder,binsize = 100,
           pulselaser = 250,plotpsd = True):
    
    In,Qn,noisefreq,fsample = ut.CalNoiseRaw(res,IQCaldata,isonres = True)
    
    pulsePointNum = round(1/pulselaser*fsample);
    NoiseSeglength = int(pulsePointNum/binsize)

    # In = np.concatenate(noiseIs)
    # Qn = np.concatenate(noiseQs)
    
    t_seg = np.arange(0,len(In))*1/fsample
    
    t_bin,In_bined = ut.AverageArray(t_seg,In,chuncksize = binsize)
    t_bin,Qn_bined = ut.AverageArray(t_seg,Qn,chuncksize = binsize)
    
    #calculate the pulse
    pulse_amp,pulse_phase = res.cal_pulse_outside(In_bined + 1j*Qn_bined,noisefreq*1e9,pulsewidth = 50,fs = 1/(t_bin[1]-t_bin[0]))
    #remove the 2*pi change
    pulse_phase = np.unwrap(pulse_phase)
    
    fpsd,pxx = sg.welch(pulse_phase-np.mean(pulse_phase),fs = 1/(t_bin[1]-t_bin[0]),nperseg = NoiseSeglength)
    fpsd,pyy = sg.welch(pulse_amp-np.mean(pulse_amp),fs = 1/(t_bin[1]-t_bin[0]),nperseg = NoiseSeglength)
    data = np.vstack([fpsd,pxx,pyy])
    
    np.savetxt(savefolder + '// psd%d.txt'%(binsize),data.T)
    
    if plotpsd == True:
        
        ut.SetDefaultPlotParam()
        plt.figure()
        plt.semilogx(fpsd,pxx)
        plt.semilogx(fpsd,pyy)
        plt.xlabel("Freq(Hz)")
        plt.ylabel("Psd($rad^2/Hz$")
        
        plt.savefig(savefolder + "//psd%d.jpg"%(binsize),dpi = 600,bbox_inches = 'tight')
    
    return data.T


def GenPSD(res,pulsefolder,IQCaldata,savefolder,binsize = 100,pulseNum = 10,
           pulselaser = 250,dt = 1e-8,t_offset = 0.001,calibrate_drift = False):
    
    pulsePointNum = round(1/pulselaser/dt);
    
    NoiseSeglength = int(pulsePointNum/binsize)
    Ip_av = np.zeros(pulsePointNum);
    # Qp_av = np.zeros(pulsePointNum)
    
    # f = open(IQfile,'rb')
    # res = pickle.load(f)
    # f.close()
    
    pxx_all = []
    pyy_all = []
    
    for i in range(pulseNum):
        
        print("Current i:",i)
        # pulsedata = res.pulseUnscaled[i]
        f = open(pulsefolder + '/%d.obj' %(i),'rb')
        pulsedata = pickle.load(f)
        f.close()
        
        I0 = res.I0;
        Q0 = res.Q0;
        freq = res.freq;
        

        I,Q,measfreq,fsample = ut.CalPulseRaw(pulsedata,IQCaldata,freq,I0,Q0,ispulse = True)
        # t = np.arange(0,len(I))*1e-08

        Ip,Qp,pulseIRaws,pulseQRaws = ut.GenAveragePulse(I,Q,dt = dt,
                                                         pulsefreq = pulselaser,
                                                         t_offset = t_offset)
        
        resfreqindx = np.argmin(np.abs(res.freq-measfreq*1e9))
        
        if i==0:

            Ip_initial = res.I[resfreqindx]
            Qp_initial = res.Q[resfreqindx]
        
        
        # Ip_av = Ip + Ip_av;
        # Qp_av = Qp + Qp_av;
        
        t_seg = np.arange(0,len(Ip_av))*dt
        
        I_noise_all = []
        Q_noise_all = []
        
    
        for pulseindx in range(len(pulseIRaws)):
            
            Iv = pulseIRaws[pulseindx]
            Qv = pulseQRaws[pulseindx]
            
            points = int((1/pulselaser/2-t_offset)/dt*3/4);
            
            Iv_noise = Iv[0:points]
            Qv_noise = Qv[0:points]
            
            t_bin,Iv_bined = ut.AverageArray(t_seg,Iv_noise,chuncksize = binsize)
            t_bin,Qv_bined = ut.AverageArray(t_seg,Qv_noise,chuncksize = binsize)
            
            
            #calibrate the offset, it assumes that the offset mainly comes from the amplifiers
            #it could also comes from the fact that the temperature of the MKIDs is rising. In this
            #case, it would be difficult to calibrate the data. 
            
            if calibrate_drift:
                Iv_bined = Iv_bined - np.mean(Iv_bined) + Ip_initial 
                Qv_bined = Qv_bined - np.mean(Qv_bined) + Qp_initial 
            
            
            I_noise_all.append(Iv_bined)
            Q_noise_all.append(Qv_bined)
        
        I_noise_all = np.concatenate(I_noise_all)
        Q_noise_all = np.concatenate(Q_noise_all)
        
        pulse_amp,pulse_phase = res.cal_pulse_outside(I_noise_all + 1j*Q_noise_all,pulsedata['freq']*1e9,pulsewidth = 50,fs = 1/(t_bin[1]-t_bin[0]))

        pulse_phase = np.unwrap(pulse_phase)
        
        fpsd,pxx = sg.welch(pulse_phase-np.mean(pulse_phase),fs = 1/(t_bin[1]-t_bin[0]),nperseg = NoiseSeglength)
        
        fpsd,pyy = sg.welch(pulse_amp-np.mean(pulse_amp),fs = 1/(t_bin[1]-t_bin[0]),nperseg = NoiseSeglength)
            
        pxx_all.append(pxx)
        pyy_all.append(pyy)
    
    pxx_average = np.zeros(np.shape(pxx))
    pyy_average = np.zeros(np.shape(pyy))


    for pxx,pyy in zip(pxx_all,pyy_all):
        
        pxx_average = pxx_average + pxx;
        pyy_average = pyy_average + pyy;

    pxx_average = pxx_average/len(pxx_all)
    pyy_average = pyy_average/len(pyy_all)
        
    
    data = np.vstack([fpsd,pxx_average,pyy_average])
    
    np.savetxt(savefolder + '//psd%d.txt'%(binsize),data.T)
    
    plt.figure()
    plt.loglog(fpsd[1:-1],pxx_average[1:-1],label = 'Phase')
    plt.loglog(fpsd[1:-1],pyy_average[1:-1],label = 'Amp')
    plt.xlabel('Freq(Hz)')
    plt.ylabel('PSD($rad^2/Hz$)')
    plt.title("dt = %fus"%(binsize*dt*1e6))
    plt.savefig(savefolder + '//psd%d.jpg' %(binsize),dpi = 300,bbox_inches = 'tight')
    # plt.close()
    
    return data.T

def GenWienerFilter(templatedata,psd,savefolder,binsize = 500,pulsetriggertime = 0.001,
                    dt = 1e-8, templatetime = 0.003,
                    templatetype = 'average', pulsedirection = 'negtive',Format = ".jpg"):
    
    # data = np.loadtxt("data 3.8885GHz/20220629133637-3.888GHz/Res Index 0/template_average_500.txt")

    # psd = np.loadtxt('20220709164518-4.9 sccm - batch 2/Res Index 1/Temp 50.0mK/noise psd bin 500.txt')
    if templatetype == 'average':
        # f = open(templatefile,'rb')
        # pulsesinglephoton = pickle.load(f)
        # f.close()

        PI = templatedata['Ia']
        PQ = templatedata['Qa']
        t_seg = templatedata['t']
        
    else: #the template type is single photon pulse

        pass
    

    t_bin,Iv_bined = ut.AverageArray(t_seg,PI,chuncksize = binsize)
    t_bin,Qv_bined = ut.AverageArray(t_seg,PQ,chuncksize = binsize)

    res = templatedata['res']

    # f.close()
    pulsefreq = (res.lmfit_vals[1] + res.lmfit_vals[0])
    amp,phase = res.cal_pulse_outside(Iv_bined + 1j*Qv_bined,pulsefreq)

    trigerindx = int(pulsetriggertime/dt/binsize)
    
    # print(trigerindx)

    phase0 = np.mean(phase[0:trigerindx])
    phase1 = phase - phase0
    phase1 = np.unwrap(phase1)
    
    amp0 = np.mean(amp[0:trigerindx])
    amp1 = amp - amp0

        
    if pulsedirection == 'positive':
        templatephase = phase1/np.max(phase1)
        
    else:
        templatephase = -phase1/np.min(phase1)
        templateamp = -amp1/np.min(amp1)
    
    templatelength = int(templatetime/dt/binsize)
    
    psdlength = (len(psd)-1)*2
    
    wifilterphase = ut.wiener(templatephase[0:templatelength],psd[:,1],psdlength)
    wifilteramp = ut.wiener(templatephase[0:templatelength],psd[:,2],psdlength)
    # wifilter = wiener(templatephase,psd[:,1],800)

    filtered_templatephase = sg.lfilter(wifilterphase,1,templatephase)
    filtered_templateamp = sg.lfilter(wifilteramp,1,templateamp)
    
    indx = np.min(filtered_templatephase)

    plt.figure()
    plt.plot(filtered_templatephase,label = 'filtered_template')
    plt.plot(templatephase[0:templatelength],label = 'template phase')
    plt.plot(wifilterphase,label = 'wiener filter phase');
    
    plt.xlabel("Index")
    plt.ylabel('Pulse Height')
    plt.legend(fontsize = 18)
    plt.savefig(savefolder + '//filtered template - phase'+Format,bbox_inches = 'tight')
    # plt.close()
    
    plt.figure()
    plt.plot(filtered_templateamp,label = 'filtered_template')
    plt.plot(templateamp[0:templatelength],label = 'template amp')
    plt.plot(wifilteramp,label = 'wiener filter amp');
    
    plt.xlabel("Index")
    plt.ylabel('Pulse Height')
    plt.legend(fontsize = 18)
    plt.savefig(savefolder + '//filtered template - amp'+Format,bbox_inches = 'tight')
    # plt.close()
    
    data = np.vstack([wifilterphase,wifilteramp])
    
    np.savetxt(savefolder + '/wienner filter-average%d.txt' %(binsize),data.T)


    return wifilterphase, wifilteramp,indx

def GenPulseStatisticsHDF(res,hdfile,wienerfilter,savefolder,IQCaldata,
                       binsize = 500,t_offset = 0.001,calibrate_drift = True,
                       pulsetype = 'phase',lowpassfiltering = False,filterorder = 10,plotbin = 0.2,Format = '.jpg'):
    
    #res: scraps.resonator obj
    
    #hdfile: the hdfile contain the pulse data
    
    #wienerfilter: the wiener filter to process the data
    
    #savefolder: directory to save the processed the data
    
    #IQCaldata: IQ Calibration data for the raw pulse data
    
    #binsize: int, the average data number
    
    #t_offset: to move the trigger time of the pulse. t_offset = 0 means the trigger of the pulse is in the center
    
    #calibrate_drift: bool, to remove the drift in the baseline or not. 
    
    #pulsetype: 'phase', or 'amp', to make the statisics using phase or amplitude
    
    #lowpassfiltering: bool, to do the lowpass filtering of the pulse data
    
    #filterorder: int, the order of the lowpass filter.
    
    #plotbin: the bin size for plotting the statistics
       
    # savefig: bool, to produce the plot of the averaged data or not
    
    #load the dataset of the pulse in the hdfile
    pulse = hdfile['pulse']
    
    #the frequency of the trigger of the laser.
    pulselaser = pulse.attrs['laserfreq']
    
    #the data of the pulse is segmented. Load the number of the groups
    NumpulseUnscaled = pulse.attrs['groupnum']
    
    #load the sample frequency of the data. The usual sample rate is about 100MHz
    dt = 1/pulse.attrs['samplefreq']

    pulse_height = []
    pulse_height_2 = []
    
    #load the DC offset of the IQ from the res
    I0 = res.I0;
    Q0 = res.Q0;
    freq = res.freq;
    
    #load the voltage gain and the offset of the oscilloscope 
    vgains = pulse['vgains'][...]
    voffsets = pulse['voffsets'][...]

    #load the readout tone frequency
    measfreq = pulse.attrs['measfreq']

    for i in range(NumpulseUnscaled):
        
        print("i:",i)
        
        #load the raw data of the IQ data, which is numpy.int16 
        pulsedata = pulse['IQ%d'%(i)][...]
        
        #scale the data from the oscillscope
        I = pulsedata[0]*vgains[0] - voffsets[0]
        Q = pulsedata[1]*vgains[1] - voffsets[1]
        
        #calibrate the IQ imbalance from the IQ mixer, i.e. the DC offset, amplitude and phase imbalance
        I,Q = IQCal.IQ_CalNoise(I,Q,measfreq/1e9,freq/1e9,I0,Q0,IQCaldata)
        
        resfreqindx = np.argmin(np.abs(res.freq-measfreq))
        
        #produce the reference for the I and Q of the pulse
        if i==0:

            Ip_initial = res.I[resfreqindx]
            Qp_initial = res.Q[resfreqindx]
        
        #segment the data by laser frequency
        Ip,Qp,pulseIRaws,pulseQRaws = ut.GenAveragePulse(I,Q,dt = dt,pulsefreq = pulselaser,t_offset = t_offset)
         
        t_seg = np.arange(0,len(Ip))*dt
        
        for pulseindx in range(len(pulseIRaws)):
            
            Iv = pulseIRaws[pulseindx]
            Qv = pulseQRaws[pulseindx]

            points = int((1/pulselaser/2 - t_offset)/dt)
            
            if calibrate_drift:
                Iv = Iv - np.mean(Iv[0:points]) + Ip_initial
                Qv = Qv - np.mean(Qv[0:points]) + Qp_initial
            
            t_bin,Iv_bined = ut.AverageArray(t_seg,Iv,chuncksize = binsize)
            t_bin,Qv_bined = ut.AverageArray(t_seg,Qv,chuncksize = binsize)
            pulse_amp,pulse_phase = res.cal_pulse_outside(Iv_bined + 1j*Qv_bined,measfreq)
            
            avenum = int((1/pulselaser/2 - t_offset)/binsize/dt)
            
            if pulsetype == 'phase':
                
                pulse_phase = np.unwrap(pulse_phase)

                phase0 = np.mean(pulse_phase[0:avenum])
            
                pulse_degree = (pulse_phase-phase0)
            
                pulse_degree = np.unwrap(pulse_degree)*180/np.pi
                pulse_wiener = sg.lfilter(wienerfilter,1,pulse_degree)
            
                indxpulse = len(wienerfilter)
            
                p_min = np.min(pulse_wiener[indxpulse-5:indxpulse+5])
            
                pulse_height.append(p_min)
            
                pulse_height_2.append(np.min(pulse_wiener[indxpulse-2:indxpulse+2]))
            
            else:
                
                amp0 = np.mean(pulse_amp[0:avenum])
            
                pulse_amp = (pulse_amp-amp0)
            
                pulse_amp = pulse_amp*180/np.pi
                pulse_wiener = sg.lfilter(wienerfilter,1,pulse_amp)
            
                indxpulse = len(wienerfilter)
            
                p_min = np.min(pulse_wiener[indxpulse-5:indxpulse+5])
            
                pulse_height.append(p_min)
            
                pulse_height_2.append(np.min(pulse_wiener[indxpulse-2:indxpulse+2]))
            

    # if pulsetype == 'phase':
    p_array = -np.array(pulse_height)
    pulsemin = np.min(p_array)
    pulsemax = np.max(p_array)

    bins = np.arange(pulsemin,pulsemax,plotbin)
    
    plt.figure()
    plt.hist(p_array,bins = bins)    

    plt.xlabel('Pulse height (deg)',fontsize = 20)
    plt.ylabel('Counts',fontsize = 20)
    
    if pulsetype == 'phase':
        plt.savefig(savefolder + '/pulse statistics-average%d'+Format,bbox_inches = 'tight')
        # plt.savefig(savefolder + '/pulse statistics-average%d.jpg'%(binsize),bbox_inches = 'tight')
        # plt.savefig(savefolder + '/pulse statistics-average%d.svg'%(binsize),bbox_inches = 'tight')
    
    else:
        plt.savefig(savefolder + '/pulse statistics-average-amp%d'+Format,bbox_inches = 'tight')
        # plt.savefig(savefolder + '/pulse statistics-average-amp%d.jpg'%(binsize),bbox_inches = 'tight')
        # plt.savefig(savefolder + '/pulse statistics-average-amp%d.svg'%(binsize),bbox_inches = 'tight')
    
    
    # plt.close()
    
    if pulsetype == 'phase':
        np.savetxt(savefolder + '/pulse_height-average%d.txt'%(binsize),pulse_height)
        np.savetxt(savefolder + '/pulse_height-average%d_2.txt'%(binsize),pulse_height_2)
        
    else:
        np.savetxt(savefolder + '/pulse_height-average-amp%d.txt'%(binsize),pulse_height)
        np.savetxt(savefolder + '/pulse_height-average-amp%d_2.txt'%(binsize),pulse_height_2)

    return pulse_height


def GenPulseStatistics(res,binsize,wienerfilter,IQCaldata,savefolder,
                       pulsefolder,calibrate_offset = True,dt = 1e-8,
                       pulselaser = 250,NumpulseUnscaled=80,t_offset = 0.001,
                       pulsetype = 'phase',lowpassfiltering = False,filterorder = 10):
    

    pulsePointNum = round(1/pulselaser/dt);
    Ip_av = np.zeros(pulsePointNum);
    Qp_av = np.zeros(pulsePointNum)

    pulse_height = []
    pulse_height_2 = []
    
    # pulse_height_amp = []
    # pulse_height_amp_2 = []

    pulseprocess = NumpulseUnscaled;


    for i in range(pulseprocess):
        
        print("i:",i)

        f = open(pulsefolder + '/%d.obj'%(i),'rb')
        pulsedata = pickle.load(f)
        f.close()
        
        
        I0 = res.I0;
        Q0 = res.Q0;
        freq = res.freq;

        I,Q,pulsefreq,fsample = ut.CalPulseRaw(pulsedata,IQCaldata,freq,I0,Q0,ispulse = True)
        # t = np.arange(0,len(I))*1e-08
        
        if lowpassfiltering == True:
            I,Q = ut.lowpassfiltering(I, sample_freq = 1/dt,Q = Q,cutoff = 100e3,filter_order = 10)
        
        Ip,Qp,pulseIRaws,pulseQRaws = ut.GenAveragePulse(I,Q,dt = dt,
                                                         pulsefreq = pulselaser,t_offset = t_offset)
        
        resfreqindx = np.argmin(np.abs(res.freq-pulsefreq*1e9))
        
        
        if i==0:

            Ip_initial = res.I[resfreqindx]
            Qp_initial = res.Q[resfreqindx]
        
        #take the data of 2ms before the pulse for the noise calculation 
        # Ip1,Qp1,noiseIRaws,noiseQRaws = ut.GenAveragePulse(I,Q,dt = 1e-8,pulsefreq = pulselaser,
                                                           # t_offset = 0.000,segtime = 0.004)
        
        Ip_av = Ip + Ip_av;
        Qp_av = Qp + Qp_av;
        
        # k = 0;
        t_seg = np.arange(0,len(Ip_av))*dt
        
        
        for pulseindx in range(len(pulseIRaws)):
            
            Iv = pulseIRaws[pulseindx]
            Qv = pulseQRaws[pulseindx]
            
            
            points = int((1/pulselaser/2 - t_offset)/dt)
            
            if calibrate_offset:
                Iv = Iv - np.mean(Iv[0:points]) + Ip_initial
                Qv = Qv - np.mean(Qv[0:points]) + Qp_initial
            
            t_bin,Iv_bined = ut.AverageArray(t_seg,Iv,chuncksize = binsize)
            t_bin,Qv_bined = ut.AverageArray(t_seg,Qv,chuncksize = binsize)
            pulse_amp,pulse_phase = res.cal_pulse_outside(Iv_bined + 1j*Qv_bined,pulsedata['freq']*1e9,pulsewidth = 50,fs = 1/(t_bin[1]-t_bin[0]))
            
            avenum = int((1/pulselaser/2 - t_offset)/binsize/dt)
            
            if pulsetype == 'phase':
                pulse_phase = np.unwrap(pulse_phase)
            
            
                phase0 = np.mean(pulse_phase[0:avenum])
            
                pulse_degree = (pulse_phase-phase0)
            
                pulse_degree = np.unwrap(pulse_degree)*180/np.pi
                pulse_wiener = sg.lfilter(wienerfilter,1,pulse_degree)
            
                indxpulse = len(wienerfilter)
            
                p_min = np.min(pulse_wiener[indxpulse-5:indxpulse+5])
            
                pulse_height.append(p_min)
            
                pulse_height_2.append(np.min(pulse_wiener[indxpulse-2:indxpulse+2]))
            
            else:
                
                amp0 = np.mean(pulse_amp[0:avenum])
            
                pulse_amp = (pulse_amp-amp0)
            
                pulse_amp = pulse_amp*180/np.pi
                pulse_wiener = sg.lfilter(wienerfilter,1,pulse_amp)
            
                indxpulse = len(wienerfilter)
            
                p_min = np.min(pulse_wiener[indxpulse-5:indxpulse+5])
            
                pulse_height.append(p_min)
            
                pulse_height_2.append(np.min(pulse_wiener[indxpulse-2:indxpulse+2]))
            

    # if pulsetype == 'phase':
    p_array = -np.array(pulse_height)
    pulsemin = np.min(p_array)
    pulsemax = np.max(p_array)
    # else:
        # p_array = -np.array(pulse_height_amp)
        # pulsemin = np.min(p_array)
        # pulsemax = np.max(p_array)
    
    bins = np.arange(pulsemin,pulsemax,0.2)
    
    plt.figure()
    plt.hist(p_array,bins = bins)    

    plt.xlabel('Pulse height (deg)',fontsize = 20)
    plt.ylabel('Counts',fontsize = 20)
    
    if pulsetype == 'phase':
        plt.savefig(savefolder + '/pulse statistics-average%d.eps'%(binsize),bbox_inches = 'tight')
        plt.savefig(savefolder + '/pulse statistics-average%d.jpg'%(binsize),bbox_inches = 'tight')
        plt.savefig(savefolder + '/pulse statistics-average%d.svg'%(binsize),bbox_inches = 'tight')
    
    else:
        plt.savefig(savefolder + '/pulse statistics-average-amp%d.eps'%(binsize),bbox_inches = 'tight')
        plt.savefig(savefolder + '/pulse statistics-average-amp%d.jpg'%(binsize),bbox_inches = 'tight')
        plt.savefig(savefolder + '/pulse statistics-average-amp%d.svg'%(binsize),bbox_inches = 'tight')
    
    
    # plt.close()
    
    if pulsetype == 'phase':
        np.savetxt(savefolder + '/pulse_height-average%d.txt'%(binsize),pulse_height)
        np.savetxt(savefolder + '/pulse_height-average%d_2.txt'%(binsize),pulse_height_2)
        
    else:
        np.savetxt(savefolder + '/pulse_height-average-amp%d.txt'%(binsize),pulse_height)
        np.savetxt(savefolder + '/pulse_height-average-amp%d_2.txt'%(binsize),pulse_height_2)
        
    
    return pulse_height

def Gaussian(x,a,mu,sigma):
    
    return a/sigma/np.sqrt(2*np.pi)*np.exp(-(x-mu)**2/2/sigma**2)



def EnergyResolution(pulseheight,savefolder,photonum = 4,binsize = 0.1,
                     peakwidth = 4,plotfigs = True,Format='.jpg'):
    
    pulseheight = np.array(pulseheight)
    
    
    pmin = np.min(-pulseheight)
    pmax = np.max(-pulseheight)

    # binsize = 0.1

    bins = np.arange(pmin,pmax+binsize ,binsize)

    a = np.histogram(-pulseheight,bins)

    x = a[1]
    x = x[:-1]
    y = a[0]

    vals = sg.find_peaks(y,width = peakwidth)

    peaks_indx = vals[0]

    center0 = x[peaks_indx[0]]
    dpeak = x[peaks_indx[1]] - center0


    gaussmodes = []
    for peak in range(photonum):
        
        prefix = 'g%d_'%(peak)
        gauss = GaussianModel(prefix = 'g%d_'%(peak))
        
        if peak == 0:
            pars = gauss.make_params()
        else:
            pars.update(gauss.make_params())
        
        if peak == 0:
            pmin = np.min(y)
            pars[prefix + 'center'].set(center0,min = pmin,max = center0 + dpeak/2)
            
            
        else:
            pars[prefix + 'center'].set(center0,min = center0 - dpeak/2,max = center0 + dpeak/2)
        
        center0 = center0 + dpeak
        
        pars[prefix + 'sigma'].set(1,min = 0.1,max = 2)
        pars[prefix + 'amplitude'].set(100,min = 0)
            
        gaussmodes.append(gauss)
        
        if peak == 0:
            mod = gauss;
        
        else:
            mod = mod + gauss
        

    out = mod.fit(y, pars, x=x)

    # print(out.fit_report(min_correl=0.5))
    
    if plotfigs == True:
        plt.figure()
    
        plt.hist(-pulseheight,bins)
        plt.plot(x + binsize/2, out.best_fit, 'r-',linewidth = 2)
    # plt.show()
        plt.xlabel('Pulse Height(deg)')
        plt.ylabel('Counts')

        deltaEs = []
        Es = []
        sigmas = []
        for i in range(photonum):
            amp = out.best_values['g%d_amplitude'%(i)]
            center = out.best_values['g%d_center'%(i)]
            sigma = out.best_values['g%d_sigma'%(i)]
        
            y = Gaussian(x,amp,center,sigma)
        
            deltaEs.append(2.3548200*sigma)
            Es.append(center)
            sigmas.append(sigma)
        
            plt.plot(x+binsize/2,y,'--',linewidth = 3,color = 'red',alpha = 0.5)
        
            peak = amp/sigma/np.sqrt(2*np.pi)
        
            plt.text(center + 0.5,peak+2,'n=%d'%(i),fontsize = 18)
        
        
        g0_center = out.best_values['g0_center']
        g1_center = out.best_values['g1_center']
        
        sigma1 = out.best_values['g1_sigma']
        
        R = 1/2/np.sqrt(2*np.log(2)) * (g1_center-g0_center)/sigma1
        # R = 1/2/np.sqrt(2*np.log(2)) * (g1_center)/sigma1
        
        plt.annotate('$\\frac{E}{\Delta E}$' + '= %1.1f @ n=1' %(R), xy=(1,1), xytext=(-130, -12), va='top',
                 xycoords='axes fraction', textcoords='offset points',fontsize = 20)

        plt.savefig(savefolder + '//Energy Resolution'+Format,bbox_inches = 'tight')
        # plt.savefig(savefolder + '//Energy Resolution.svg',bbox_inches = 'tight')
    
        # plt.savefig(savefolder + '//Energy Resolution.jpg',dpi = 600,bbox_inches = 'tight')
        # print('fig saved')
    
    return out,Es,sigmas
    
    
def GenSinglePhotonPulse(res,IQCaldata,Ers,Sigmas,wienerfilter,savefolder,
                         pulsefolder,pulseheight = None,binsize = 500,
                         calibrate_offset = True,dt = 1e-8,pulselaser = 250,
                         NumpulseUnscaled=80,t_offset = 0.001,genrawdataplot = True,
                         rawdataplotnum = 2,plot_figs = True):

    pulsePointNum = round(1/pulselaser/dt);
    Ip_av = np.zeros(pulsePointNum);
    Qp_av = np.zeros(pulsePointNum)

    # pulse_height = []
    # pulse_height_2 = []

    pulseprocess = NumpulseUnscaled;
    
    photonums = len(Ers) + 1
    
    Isp = [Ip_av]*photonums
    Qsp = [Qp_av]*photonums
    
    pulsenums = [0]*photonums
    
    if genrawdataplot == True:
        rawdataplotted = [0]*photonums
        # rawdataplotnum
    # sp_pulse = 
    pulseindx = 0;

    for i in range(pulseprocess):
        
        print("i:",i)

        f = open(pulsefolder + '/%d.obj'%(i),'rb')
        pulsedata = pickle.load(f)
        f.close()
        
        
        I0 = res.I0
        Q0 = res.Q0
        freq = res.freq
        
        
        I,Q,pulsefreq,fsample = ut.CalPulseRaw(pulsedata,IQCaldata,freq,I0,Q0,ispulse = True)
        # t = np.arange(0,len(I))*1e-08

        Ip,Qp,pulseIRaws,pulseQRaws = ut.GenAveragePulse(I,Q,dt = dt,
                                                         pulsefreq = pulselaser,t_offset = t_offset)
        
        resfreqindx = np.argmin(np.abs(res.freq-pulsefreq*1e9))
        
        
        if i==0:

            Ip_initial = res.I[resfreqindx]
            Qp_initial = res.Q[resfreqindx]
        
        #take the data of 2ms before the pulse for the noise calculation 
        # Ip1,Qp1,noiseIRaws,noiseQRaws = ut.GenAveragePulse(I,Q,dt = 1e-8,pulsefreq = pulselaser,
                                                           # t_offset = 0.000,segtime = 0.004)
        
        # Ip_av = Ip + Ip_av;
        # Qp_av = Qp + Qp_av;
        
        # k = 0;
        t_seg = np.arange(0,len(Ip_av))*dt
        for pulseindx in range(len(pulseIRaws)):
            
            Iv = pulseIRaws[pulseindx]
            Qv = pulseQRaws[pulseindx]
            
            if calibrate_offset:
                
                points = int((1/pulselaser/2 - t_offset)/dt)
                Iv = Iv - np.mean(Iv[0:points]) + Ip_initial
                Qv = Qv - np.mean(Qv[0:points]) + Qp_initial
            
            
            if pulseheight is None or genrawdataplot == True:
                
                t_bin,Iv_bined = ut.AverageArray(t_seg,Iv,chuncksize = binsize)
                t_bin,Qv_bined = ut.AverageArray(t_seg,Qv,chuncksize = binsize)
                pulse_amp,pulse_phase = res.cal_pulse_outside(Iv_bined + 1j*Qv_bined,pulsedata['freq']*1e9,pulsewidth = 50,fs = 1/(t_bin[1]-t_bin[0]))
                
                pulse_phase = np.unwrap(pulse_phase)
            
                avenum = int((1/pulselaser/2 - t_offset)/binsize/dt)
                phase0 = np.mean(pulse_phase[0:avenum])
            
                pulse_degree = (pulse_phase-phase0)
            
                pulse_degree = np.unwrap(pulse_degree)*180/np.pi
                pulse_wiener = sg.lfilter(wienerfilter,1,pulse_degree)
            
                indxpulse = len(wienerfilter)
            
                phCurrent = -np.min(pulse_wiener[indxpulse-5:indxpulse+5])
            
            else:
                
                phCurrent = -pulseheight[pulseindx]
                pulseindx += 1
            
            photonum = -1
            for indx,(er,sigma) in enumerate(zip(Ers,Sigmas)):
                
                if indx == 0:
                    if phCurrent < er + sigma*2.355/2:
                        
                        Isp[indx] = Isp[indx] + Iv
                        Qsp[indx] = Qsp[indx] + Qv
                        
                        pulsenums[indx] +=  1
                        photonum = 0
                        
                        break
                        
                elif indx <= len(Ers) - 1:
                    if phCurrent > er - sigma*2.355/2 and phCurrent < er + sigma*2.355/2:
                        
                        Isp[indx] = Isp[indx] + Iv
                        Qsp[indx] = Qsp[indx] + Qv
                        
                        pulsenums[indx] +=  1
                        photonum = indx
                        
                        break
                    
                else:
                    if phCurrent > Ers[-1] + Sigmas[-1]*2.355/2:
                        Isp[indx] = Isp[indx] + Iv
                        Qsp[indx] = Qsp[indx] + Qv
                    
                        pulsenums[indx] +=  1
                        photonum = indx
                    break
            
            if photonum == -1:
                continue
            
            if genrawdataplot == True:
                
               
                if rawdataplotted[photonum] == rawdataplotnum:
                    # rawdataplotted[photonum] = 
                    continue
                else:
                    rawdataplotted[photonum] += 1
                
                
                plt.figure()
                plt.plot(t_bin*1000,pulse_degree,color = 'blue',label = 'raw')
                plt.plot(t_bin*1000,pulse_wiener,color = 'red',label = 'wiener filtered')
                
                plt.xlabel('Time(ms)')
                plt.ylabel('Pulse Height(deg)')
                
                plt.legend(fontsize = 15)
                plt.title("%d Photon Event" %(photonum),fontsize = 20)
                
                plt.savefig(savefolder + '//%d Photon Event_%d.eps' %(photonum,rawdataplotted[photonum]),bbox_inches = 'tight')
                plt.savefig(savefolder + '//%d Photon Event_%d.jpg' %(photonum,rawdataplotted[photonum]),dpi = 600,bbox_inches = 'tight')
                
                # plt.close()
        
        #average the pulse number
        
    for i in reversed(range(len(pulsenums))):
        
        if pulsenums[i] == 0:
            continue
            
        Isp[i] = Isp[i]/pulsenums[i]
        Qsp[i] = Qsp[i]/pulsenums[i]
        
        
    res.noiseUnscaled = []
        
    data = {'Isp':Isp,
            'Qsp':Qsp,
            'Res':res,
            'pulsefreq':pulsedata['freq'],
            't_offset':t_offset,
            'pulsetriggertime':1/pulselaser/2 - t_offset,
            'dt':dt}
        
    f = open(savefolder + '/singlephotondata.obj','wb')
        
    pickle.dump(data,f)
        
    f.close()
    
    if plot_figs == True:
        
        PlotSingplePhotonPulse(data,savefolder,closefig = True)
        # plt_colors, sm = ut.GenColorMap(range(len(pulsenums)))
        # plt.figure()
                    
        # for i in reversed(range(len(pulsenums))):
        
        #     if pulsenums[i] == 0:
        #         continue
        #     pulse_amp,pulse_phase = res.cal_pulse_outside(Isp[i] + 1j*Qsp[i],pulsedata['freq']*1e9,pulsewidth = 50,fs = 1/(t_bin[1]-t_bin[0]))

        #     avenum = int((1/pulselaser/2 - t_offset)/dt)
        #     pulse_phase = np.unwrap(pulse_phase)
        #     phase0 = np.mean(pulse_phase[0:avenum])
        
        #     pulse_phase = np.unwrap(pulse_phase - phase0)
        
        #     plt.plot(t_seg*1000-t_offset*1000,(pulse_phase)*180/np.pi,
        #          label = '%d photons'%(i),color = plt_colors[i])
            
        #     plt.xlabel('Time(ms)')
        #     plt.ylabel('Pulse Height(deg)')
        #     plt.legend(fontsize = 15)
        
        
        # plt.savefig(savefolder + '//Single Photon Average.eps',bbox_inches = 'tight')
        # plt.savefig(savefolder + '//Single Photon Average.jpg',dpi = 600,bbox_inches = 'tight')
            
        # plt.close()
        
def PlotSingplePhotonPulse(spdata,savefolder,closefig = True):
    
    # data = {'Isp':Isp,
    #         'Qsp':Qsp,
    #         'Res':res,
    #         'pulsefreq':pulsedata['freq'],
    #         't_offset':t_offset,
    #         'pulsetriggertime':1/pulselaser/2 - t_offset,
    #         'dt':dt}
        
    Isp = spdata['Isp']
    Qsp = spdata['Qsp']
    res = spdata['Res']
    t_trigger =  spdata['pulsetriggertime']
    t_offset = spdata['t_offset']
    dt = spdata['dt']
    pulsefreq = spdata['pulsefreq']
    
    avenum = int(t_trigger/dt)
    
    plt_colors, sm = ut.GenColorMap(range(len(Isp)-1))
    fig, ax1 = plt.subplots()
    t_seg = np.arange(0,len(Isp[0]))*dt
    
    pmax = []
    for i in reversed(range(len(Isp))):
    
        # if pulsenums[i] == 0:
            # continue
        
        if np.sum(np.abs(Isp[i])) < 1e-10:
            continue
        
        pulse_amp,pulse_phase = res.cal_pulse_outside(Isp[i] + 1j*Qsp[i],pulsefreq*1e9,pulsewidth = 50,fs = 1/dt)

        # avenum = int((1/pulselaser/2 - t_offset)/dt)
        pulse_phase = np.unwrap(pulse_phase)
        
        phase0 = np.mean(pulse_phase[0:avenum])
    
        pulse_phase = np.unwrap(pulse_phase - phase0)
        
        pmax.append(np.min(pulse_phase))
    
        ax1.plot(t_seg*1000-t_offset*1000,(pulse_phase)*180/np.pi,
             label = '%d photons'%(i),color = plt_colors[i])
        
    ax1.set_xlabel('Time(ms)')
    ax1.set_ylabel('Pulse Height(deg)')
        # ax1.legend(fontsize = 15)
    cbar = plt.colorbar(sm,ax = ax1)
    cbar.ax.set_ylabel('Photon number', rotation=270,labelpad = 20)
    photonum = np.array([1,2,3,4])
    
    pmax.reverse()
    pmax = np.array(pmax)
    
    a = np.polyfit(photonum,pmax[1:-1]*180/np.pi,1)

    photonum = np.array([0,1,2,3,4,5])

    # plt.plot(photonum,a[0]*photonum + a[1])
    
    left, bottom, width,height = [0.42,0.3,0.3,0.3]
    ax2 = fig.add_axes([left,bottom,width,height])
    
    ax2.plot(pmax*180/np.pi,'s')
    ax2.plot(photonum,(a[0]*photonum + a[1]))
    ax2.set_xlabel('Photo number',fontsize = 12)
    ax2.set_ylabel('Pulse Height(deg)',fontsize = 12)
    
    plt.setp(ax2.get_xticklabels(), fontsize=12)
    plt.setp(ax2.get_yticklabels(), fontsize=12)
    
    plt.savefig(savefolder + '//Single Photon Average.eps',bbox_inches = 'tight')
    plt.savefig(savefolder + '//Single Photon Average.jpg',dpi = 600,bbox_inches = 'tight')
    
    # if closefig == True:
    #     plt.close()     
        
    
        
    return fig,pmax

