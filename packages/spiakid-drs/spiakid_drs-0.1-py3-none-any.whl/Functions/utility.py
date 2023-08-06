import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import re
from scipy import signal
import scipy as sp
import Functions.IQCalibration as IQCal
import os
import pickle


#the following three function comes from Mazin's Lab*********************
def covariance_from_psd(psd, size=None, window=None, dt=1.):
    autocovariance = np.real(np.fft.irfft(psd / 2., window) / dt)  # divide by 2 for single sided PSD
    if size is not None:
        autocovariance = autocovariance[:size]
    covariance = sp.linalg.toeplitz(autocovariance)
    return covariance


def filter_cutoff(filter_, cutoff):
    """
    This function addresses a problem encountered when generating filters from
    oversampled data. The high frequency content of the filters can be
    artificially large due to poor estimation of the noise and template.

    In this case it is useful to remove frequencies above the cutoff from the
    filter. Only use this function when addressing the above issue and if the
    majority of the signal frequencies are < cutoff.

    It is best to avoid this procedure if possible since removing the high
    frequency content will artificially make the filter periodic, throws away
    some information in the signal, and may negatively influence some of the
    intended filter properties.
    """
    freq = np.fft.rfftfreq(filter_.shape[0], d=1)
    filter_fft = np.fft.rfft(filter_, axis=0)
    filter_fft[freq > cutoff, ...] = 0
    filter_ = np.fft.irfft(filter_fft, filter_.shape[0], axis=0)
    return filter_

def wiener(*args, **kwargs):
    """
    Create a filter that minimizes the chi squared statistic when aligned
    with a photon pulse.

    Args:
        template:  numpy.ndarray
            The template with which to construct the filter.
        psd:  numpy.ndarray
            The power spectral density of the noise.
        nwindow: integer
            The window size used to compute the PSD.
        nfilter: integer (optional)
            The number of taps to use in the filter. The default is to use
            the template size.
        cutoff: float (optional)
            Set the filter response to zero above this frequency (in units of
            1 / dt). If False, no cutoff is applied. The default is False.
        fft: boolean (optional)
            If True, the filter will be computed in the Fourier domain, which
            could be faster for very long filters but will also introduce
            assumptions about periodicity of the signal. In this case, the
            psd must be the same size as the filter Fourier transform
            (nfilter // 2 + 1 points). The default is False, and the filter is
            computed in the time domain.
        normalize: boolean (optional)
            If False, the template will not be normalized. The default is True
            and the template is normalized to a unit response.
    Returns:
        filter_: numpy.ndarray
            The computed wiener filter.
    """
    # collect inputs
    template, psd, nwindow = args[0], args[1], args[2]
    nfilter = kwargs.get("nfilter", len(template))
    cutoff = kwargs.get("cutoff", False)
    fft = kwargs.get("fft", False)
    normalize = kwargs.get("normalize", True)

    # need at least this long of a PSD
    if nwindow < nfilter:
        raise ValueError("The psd must be at least as long as the length of the FFT of the filter")

    # pad the template if it's shorter than the filter (linear ramp to avoid discontinuities)
    if nfilter > len(template):
        template = np.pad(template, (0, nfilter - len(template)), mode='linear_ramp')
    # truncate the template if it's longer than the filter
    elif nfilter < len(template):
        template = template[:nfilter]

    if fft:  # compute the filter in the frequency domain (introduces periodicity assumption, requires nwindow=nfilter)
        if nwindow != nfilter:
            raise ValueError("The psd must be exactly the length of the FFT of the filter to use the 'fft' method.")
        template_fft = np.fft.rfft(template)
        filter_ = np.fft.irfft(np.conj(template_fft) / psd, nwindow)  # must be same size else ValueError
        filter_ = np.roll(filter_, -1)  # roll to put the zero time index on the far right

    else:  # compute filter in the time domain (nfilter should be << nwindow for this method to be better than fft)
        covariance = covariance_from_psd(psd, size=nfilter, window=nwindow)
        filter_ = np.linalg.solve(covariance, template)[::-1]

    # remove high frequency filter content
    if cutoff:
        filter_ = filter_cutoff(filter_, cutoff)

    # normalize
    if normalize:
        filter_ /= -np.matmul(template, filter_[::-1])
    else:
        filter_ *= -1   # "-" to give negative pulse heights after filtering
    return filter_

#the above three function comes from Mazin's Lab*********************


# def GenWienerFilter(template)
def CalNoiseRaw(res,IQCaldata,isonres = True):
    
    noiseIs = []
    noiseQs = []
    
    freq = res.freq;
    I0 = res.I0;
    Q0 = res.Q0
    
    if isonres == True:
        noisearray = res.noiseUnscaled
    else:
        noisearray = res.noiseOffresUnscaled
    
    for noisedata in noisearray:
    # pulsefreq = res.pulseUnscaled
        noisefreq = noisedata['freq']
        voffset = noisedata['voffsets']
        vgains = noisedata['vgains']
        
        # print("pulsefreq:",pulsefreq)
        
        fsample = 1/noisedata['dt']
        I = noisedata['traces'][0]*vgains[0] - voffset[0]
        Q = noisedata['traces'][1]*vgains[1] - voffset[1]
        
        I,Q = IQCal.IQ_CalNoise(I,Q,noisefreq,freq/1e9,I0,Q0,IQCaldata)
        
        noiseIs.append(I)
        noiseQs.append(Q)
        
    noiseIs = np.concatenate(noiseIs)
    noiseQs = np.concatenate(noiseQs)
    
        
    return noiseIs,noiseQs,noisefreq,fsample

def CalNoiseHDf(res,hdfile,IQCaldata,isonres = True):
    
    #calibrate the noise data from a hdf file
    
    noiseIs = []
    noiseQs = []
    
    freq = res.freq;
    I0 = res.I0;
    Q0 = res.Q0
    
    if isonres == True:
        # noisearray = res.noiseUnscaled
        noisedata = hdfile['noise']
    else:
        # noisearray = res.noiseOffresUnscaled
        noisedata = hdfile['noiseoffres']
        
    segnum = noisedata.attrs['groupnum']
    
    noisefreq = noisedata.attrs['measfreq']/1e9
    
    voffsets = noisedata['voffsets'][...]
    vgains = noisedata['vgains'][...]
    
    for i in range(segnum):
    # pulsefreq = res.pulseUnscaled
        
        # print("pulsefreq:",pulsefreq)
        IQdata = noisedata['IQ%d'%(i)][...]
        
        # fsample = 1/noisedata['dt']
        I = IQdata[0]*vgains[0] - voffsets[0]
        Q = IQdata[1]*vgains[1] - voffsets[1]
        
        I,Q = IQCal.IQ_CalNoise(I,Q,noisefreq,freq/1e9,I0,Q0,IQCaldata)
        
        noiseIs.append(I)
        noiseQs.append(Q)
        
    noiseIs = np.concatenate(noiseIs)
    noiseQs = np.concatenate(noiseQs)
    
        
    return noiseIs,noiseQs

def CalPulseRaw(pulsedata,IQCaldata,freq,I0,Q0,ispulse = True):
    
    pulsefreq = pulsedata['freq']
    voffset = pulsedata['voffsets']
    vgains = pulsedata['vgains']
    
    # print("pulsefreq:",pulsefreq)
    
    fsample = 1/pulsedata['dt']
    I = pulsedata['traces'][0]*vgains[0] - voffset[0]
    Q = pulsedata['traces'][1]*vgains[1] - voffset[1]
    
    I,Q = IQCal.IQ_CalNoise(I,Q,pulsefreq,freq/1e9,I0,Q0,IQCaldata)
    
    return I,Q,pulsefreq,fsample

def CombineBins(freq,spectrum,bins = [50,1e3,1e4,1e5,1e6],resolutions = [1,10,100,1000,10000]):
    
    indx_bins = []
    
    indx_bins.append(0)
    
    for i,freqseg in enumerate(bins):
        
        indx_bin = np.argmin(np.abs(freq-freqseg))
        
        if indx_bin == len(freq): #check if the bin is the end of the freq
            
            if indx_bins[i-1] == indx_bin:
                
                break
            
        indx_bins.append(indx_bin)
        
        
    if indx_bins[-1] < len(freq)-1: #check if the bin is the end of the freq
        
        bins.append(freq[-1])
         
        indx_bins.append(len(freq))
        
        resolutions.append(resolutions[-1])
        
    if len(bins) > len(indx_bins):
        
        bins = bins[0:len(indx_bins)]
        resolutions = resolutions[0:len(indx_bins)]
    
    
    df = freq[1]-freq[0]
    
    NumBinned = 0
    
    NumBins = []
    
    for i, freqseg in enumerate(bins):
        
        resolution = resolutions[i]
        
        if df > resolutions[i]:
            
            resolution = df
        
        if i == 0:
            NumBinned = NumBinned + np.floor(freqseg/resolution)
            NumBins.append(np.floor(freqseg/resolution))
        else:
            NumBinned = NumBinned + np.floor((freqseg - bins[i-1])/resolution)
            NumBins.append(np.floor((freqseg - bins[i-1])/resolution))
        
        # NumBins.append(NumBinned)
            
    freq_binned = np.zeros(int(NumBinned))
    
    spectrum_binned = np.zeros(int(NumBinned))
        
    
    count = 0
    
    for i, freqseg in enumerate(bins):
        
        resolution = resolutions[i]
        
        indx = indx_bins[i]
            
        if df > resolutions[i]:
            
            resolution = df
            
        # Numbin = int(np.floor(freqseg / resolution))
        
        Numbin = int(NumBins[i]) - 1
            
        Bincombine = int(np.floor(resolution/df))
            
        for jN in range(Numbin):
                
             freq_binned[count] = freq[indx + jN*Bincombine] 
             spectrum_binned[count] = np.sum(spectrum[indx+jN*Bincombine:indx+(jN+1)*Bincombine])/Bincombine
             
             count = count + 1
             
             
             
        
    return freq_binned[0:count],spectrum_binned[0:count]    

def ExtractDatafromString(data_string):
    
    data_string = re.findall('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[+-]?\ *[0-9]+)?',data_string)
    
#    data_string = re.findall('-?\d\.?\d*[Ee][+\-]?\d+',data_string);
    
    data = [float(i) for i in data_string]
    
    return data

def IQ_binary(filename):
    
    data = np.fromfile(filename,dtype=float,count = -1,sep = '')
    data_len = int((len(data)-1)/2)
    
    
    # print(data[0])
    # print(data[1])
    
    time = data[0]*np.arange(0,data_len)
    
    if len(data)>data_len*2+1:
        I = data[2:data_len+2]
        Q = data[data_len+2:2*data_len+2]
    else:
        I = data[1:data_len+1]
        Q = data[data_len+1:2*data_len+1]

    # pulse_phase = pulse_phase[mask]

        
        
    # plt.figure()
    
    # plot()
    
    return time,I, Q

def Truncate_Pulse(I,Q,dt = 1,t_start = -np.inf,t_stop = np.inf):
    
    data_len = len(I)
    time = dt*np.arange(0,data_len)

    # mask = (time)
    mask = (time >= t_start) * (time <= t_stop)
        
    I = I[mask]
    Q = Q[mask]
    
    return I,Q

def IQBinaryIntCal(FileIntCal):
    
    file = open(FileIntCal,'r')
    Lines = file.readlines()
    
    sampleT = ExtractDatafromString(Lines[0])
    samplePoint = ExtractDatafromString(Lines[1])
    vgains = ExtractDatafromString(Lines[2])
    voffsets =  ExtractDatafromString(Lines[3])
    
    return sampleT[0],int(samplePoint[0]),vgains,voffsets
        
    

def IQBinaryInt(FileInt,FileIntCal):
    
    data = np.fromfile(FileInt,dtype = np.short,count = -1)
    
    data_len = int(len(data)/2)
    
    sampleT, samplePoint,vgains,voffsets = IQBinaryIntCal(FileIntCal)
    
    time = sampleT*np.arange(0,data_len)
    I = data[0:data_len]*vgains[0] - voffsets[0]
    Q = data[data_len:2*data_len]*vgains[1] - voffsets[1]
    
    return time,I,Q
    
def lowpassfiltering(I,sample_freq,Q = None,cutoff = None,filter_order = 10):
    
    if cutoff == None:
        cutoff = sample_freq*0.4
    # print("sample_freq:",sample_freq)
#    cutoff = cutoff/sample_freq
    sos = signal.butter(filter_order, cutoff , 'lowpass', fs = sample_freq,output='sos' )
    
    I = signal.sosfilt(sos,I)
    
    if Q is None:
        
        return I
    
    else:
        
        Q = signal.sosfilt(sos,Q)

        return I,Q
    
    return I

def AverageArray(time,array,chuncksize = 10):
    
    newarraysize = int(np.floor(len(array)/chuncksize));
    newarray = np.zeros(newarraysize)
    newtimearray = np.zeros(newarraysize)
    for i in range(newarraysize):
        newarray[i] = np.mean(array[i*chuncksize:(i+1)*chuncksize])
        newtimearray[i] = time[i*chuncksize]
        
    return newtimearray,newarray
             
def GenReslist(datafolder,select_by = "Temp",InAtten = 30,Temp = 50,IDString = ["_cal.obj"]):

    reslist = []
    resfreq = []
    temp = []
    resfilenames = []
    
    
    if select_by == "Temp":
        
        AttenString = "Inatten{0:.0f}".format(InAtten)
        
        IDString.append(AttenString)
        
        folders = os.listdir(datafolder)
        
        tempfolders = []
        
        #Get the temp folders
        for folder in folders:
            
            if "mK" in folder and os.path.isdir(datafolder + "//" + folder): 
                
                tempfolders.append(datafolder + "//" + folder)
                
        # print(tempfolders)
                
        #Get the res filenames        
        for folder in tempfolders:
            
            files = os.listdir(folder)
            
            
            
            for file in files:
                
                correct_file = True
                
                for string in IDString:
                
                    correct_file = correct_file*(string in file)
                
                if correct_file:
                    resfilenames.append(folder + "//" + file)
        
                
        if resfilenames != []:
            
            # print(resfilenames)
            for file in resfilenames:
            
                f = open(file,'rb')
                res = pickle.load(f)
                f.close()
                
                reslist.append(res)
                
                temp.append(res.temp)
                
                resfreq.append(res.lmfit_vals[1])
                
            indxs = np.argsort(np.array(temp))    
            
            temp = [temp[k] for k in indxs]
            resfreq = [resfreq[k] for k in indxs]
            reslist = [reslist[k] for k in indxs]
                
    return temp,resfreq,reslist                  
                

def GenReslistobj(datafolder,select_by = "temp",InAtten = 30,Temp = 50,
                  AttenStringFormat = "Inatten{0:.0f}",TempStringFormat = "Res{0:.0f}mK",IDString = [".obj"]):

    reslist = []
    resfreq = []
    temp = []
    resfilenames = []
    
    
    if select_by == "temp":

        AttenString = AttenStringFormat.format(InAtten)
        
        IDString.append(AttenString)
        
        folders = os.listdir(datafolder)
        
        tempfolders = []
        
        #Get the temp folders
        for folder in folders:
            
            if "mK" in folder and os.path.isdir(datafolder + "//" + folder): 
                
                tempfolders.append(datafolder + "//" + folder)
        #Get the res filenames        
        for folder in tempfolders:
            
            files = os.listdir(folder)
            
            
            
            for file in files:
                
                correct_file = True
                
                for string in IDString:
                
                    correct_file = correct_file*(string in file)
                
                if correct_file:
                    resfilenames.append(folder + "//" + file)
        
                
        if resfilenames != []:
            for file in resfilenames:
            
                f = open(file,'rb')
                res = pickle.load(f)
                f.close()
                
                reslist.append(res)
                
                temp.append(res.temp)
                
                resfreq.append(res.lmfit_vals[1])
                
            indxs = np.argsort(np.array(temp))    
            
            temp = [temp[k] for k in indxs]
            resfreq = [resfreq[k] for k in indxs]
            reslist = [reslist[k] for k in indxs]
    
    if select_by == "pwr":
        
        TempString = TempStringFormat.format(Temp)
        
        IDString.append(TempString)
        
        folders = os.listdir(datafolder)
        
        tempfolders = []
        
        #Get the temp folders
        for folder in folders:
            
            if "mK" in folder and os.path.isdir(datafolder + "//" + folder): 
                
                tempfolders.append(datafolder + "//" + folder)
        #Get the res filenames        
        for folder in tempfolders:
            
            files = os.listdir(folder)

            for file in files:
                
                correct_file = True
                
                for string in IDString:
                
                    correct_file = correct_file*(string in file)
                
                if correct_file:
                    resfilenames.append(folder + "//" + file)
        
                
        if resfilenames != []:
            for file in resfilenames:
            
                f = open(file,'rb')
                res = pickle.load(f)
                f.close()
                
                reslist.append(res)
                
                temp.append(res.temp)
                
                resfreq.append(res.lmfit_vals[1])
                
            indxs = np.argsort(np.array(temp))    
            
            temp = [temp[k] for k in indxs]
            resfreq = [resfreq[k] for k in indxs]
            reslist = [reslist[k] for k in indxs]
    
    
    
    
    
    return temp,resfreq,reslist, resfilenames                
                    

def ExtractLmfitParams(reslist,param = 'f0'):
    
    if param in reslist[0].lmfit_labels:
        indx = reslist[0].lmfit_labels.index(param)
    else:
        print("No %s in the reslist" %(param))
        return [];
    
    params = []
    
    for res in reslist:
        
        params.append(res.lmfit_vals[indx])

    return params


def GetSortIndex(params,desending = True):
    
    indx = sorted(range(len(params)), key=lambda k: params[k])
    
    if desending == False:
        indx.reverse()
    
    return indx
        
def GenColorMap(params,colormap = 'jet'):
    
    color_gen = plt.get_cmap(colormap)
    
    if len(params) > 1:
        
        plt_color = [color_gen((param-min(params))/(max(params)-min(params))) for param in params]
        
        # plt_color = color_gen(params*1.0/max(params))
    else:
        plt_color = [color_gen(0)]
        
    cbar_norm= mpl.colors.Normalize(vmin=min(params), vmax=max(params))

    sm = mpl.cm.ScalarMappable(cmap = colormap,norm = cbar_norm)
    
    return plt_color,sm
    
def GetResTemp(folder,tempindx = 0):
    
    files = os.listdir(folder)
    
    temps = []
    for file in files:
        
        params = ExtractDatafromString(file)
        
        temps.append(params[tempindx])
        
    return temps
        
def SetDefaultPlotParam():
    
    mpl.rcParams['lines.linewidth'] = 2
    # mpl.rcParams['lines.color'] = 'r'    
    mpl.rcParams['axes.labelsize'] = 20;
    
    mpl.rcParams['xtick.labelsize'] = 15;
    mpl.rcParams['ytick.labelsize'] = 15;
    
    mpl.rcParams['font.family'] = 'Times New Roman'
    mpl.rcParams['mathtext.fontset'] = 'custom'
    mpl.rcParams['mathtext.rm'] = 'Times New Roman'
    mpl.rcParams['mathtext.it'] = 'Times New Roman:italic'
    mpl.rcParams['mathtext.bf'] = 'Times New Roman:bold'
    # mpl.rcParams.update({
    # "text.usetex": True,
    # "font.family": "time new roman"})


def GetPulseMaxMin(reslist,pulsewidths = [50]):
    
    pulsemins = []
    pulsemaxs = []
    
    pulsemins_indx = []
    pulsemaxs_indx = []
    
    for pulsewidth in pulsewidths:
        
        indx = reslist[0].pulseWidths.index(pulsewidth)
        
        pulsemin = []
        pulsemax = []
        
        pulseminindx = []
        pulsemaxindx = []
        
        for res in reslist:
            
            pulsephase = res.pulsePhases[indx]
            phase0 = np.mean(np.unwrap(pulsephase[0:10000]))
            
            dphase = np.unwrap(pulsephase - phase0);
            
            pulsemin.append(np.min(dphase))
            pulseminindx.append(np.argmin(dphase))
            
            pulsemax.append(np.max(dphase))
            pulsemaxindx.append(np.argmax(dphase))
            
        pulsemins.append(pulsemin)
        pulsemaxs.append(pulsemax)
        
        pulsemins_indx.append(pulseminindx)
        pulsemaxs_indx.append(pulsemaxindx)
        
    return pulsemins,pulsemaxs,pulsemins_indx,pulsemaxs_indx
    
def CalPowerResponse(oresponse,opower):

    oresponse = np.array(oresponse)
    opower = np.array(opower)
    
    response = []
    
    for i in range(oresponse.shape[1]):
        
        oresponse_i = oresponse[:,i]
        
        fitresult = np.polyfit(opower,oresponse_i,1)
        
        response.append(fitresult[0])
        
        
    return response
    
def GenAveragePulse(I,Q,dt = 1e-8,pulsefreq = 250,t_offset = 0,segtime = 0):
    
    
    NumPointPulse = round(1/pulsefreq/dt);
    
    # pulseI = np.zeros(NumPointPulse);
    # pulseQ = np.zeros(NumPointPulse);
    
    Pointoffset = round(t_offset/dt)
    
    pulseNum = int((len(I)-Pointoffset)/NumPointPulse)
    
    pulseIRaws = []
    pulseQRaws = []
    
    if segtime > 0 and segtime<1/pulsefreq:
        segpoints = round(segtime/dt)
        
    else:
        segpoints = NumPointPulse
        
    pulseI = np.zeros(segpoints);
    pulseQ = np.zeros(segpoints);    
        
    
    for i in range(pulseNum):
        
        I_current = I[(i*NumPointPulse+Pointoffset):(i*NumPointPulse+Pointoffset+segpoints)]
        Q_current = Q[(i*NumPointPulse+Pointoffset):(i*NumPointPulse+Pointoffset+segpoints)]
        pulseIRaws.append(I_current)
        pulseQRaws.append(Q_current)
        
        pulseI = pulseI + I_current
        pulseQ = pulseQ + Q_current
        
        # currentI = 
        
        
    pulseI = pulseI/pulseNum;
    pulseQ = pulseQ/pulseNum;
    
    return pulseI, pulseQ, pulseIRaws,pulseQRaws

# def GenAveragePulse(I,Q,dt = 1e-8,pulsefreq = 250):
    
#     NumPointPulse = round(1/pulsefreq/dt);
    
#     pulseI = np.zeros(NumPointPulse);
#     pulseQ = np.zeros(NumPointPulse);
    
    
#     pulseNum = round(len(I)/NumPointPulse)
    
#     for i in range(pulseNum):
        
#         pulseI = pulseI + I[i*NumPointPulse:(i+1)*NumPointPulse]
#         pulseQ = pulseQ + Q[i*NumPointPulse:(i+1)*NumPointPulse]
        
#     pulseI = pulseI/pulseNum;
#     pulseQ = pulseQ/pulseNum;
    
#     return pulseI, pulseQ
       
    
    