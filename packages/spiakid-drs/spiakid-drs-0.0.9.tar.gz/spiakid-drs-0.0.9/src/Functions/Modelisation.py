import numpy as np
import h5py
import matplotlib.pyplot as plt
import lmfit as lf
import glob
import scipy.signal as sps
from scipy import interpolate as interp

import Functions.resonator as a
import Functions.SinglePhotonProcess as spp
import Functions.cmplxIQ as fitmodel

def Data_read(Data,Plot_path,Plot_Format):
    f = h5py.File(Data,'r')
#get the temp and readout power of the measurement
    temp = f['header'].attrs['temp']
    pwr = f['header'].attrs['power']

#get frequency, I and Q of the resonator 
    freq = f['resonator/freq'][...]
    I = f['resonator/I'][...]
    Q = f['resonator/Q'][...]

    I0 = f['resonator/I0'][...]
    Q0 = f['resonator/Q0'][...]

    #get the IQ calibation data for the noise and pulse data
    IQCaldata = f['calibration/IQCaldata'][...]

    #create a resonator object
    res = a.Resonator('1', temp, pwr, freq, I, Q,I0 = I0,Q0 = Q0)
    #fit the resonator with S21 (transmission)
    res.load_params(fitmodel.cmplxIQ_params)
    res.do_lmfit(fitmodel.cmplxIQ_fit)

    t_offset = 0.001
    binsize = 500

    templatetime = 0.002

    laserfreq = f['pulse'].attrs['laserfreq']
    pulsetriggertime = 1/laserfreq/2 - t_offset
    savefolder = Plot_path
    samplefreq = f['pulse'].attrs['samplefreq']

    #generate the averaged pulse data as the template
    avedata = spp.GenPulseAverageWithHDF(res,f,savefolder,IQCaldata,calibrate_drift = True, t_offset = t_offset,savefig = True,Format=Plot_Format)

    #generate the psd (Power Spectral Density) of the resonator
    psd = spp.GenPSDWithHDF(res,f,savefolder,IQCaldata,binsize = binsize,pulselaser = laserfreq,Format=Plot_Format)


    #generate the wiener filter for both amplitude and phase
    wifilterphase, wifilteramp,indx = spp.GenWienerFilter(avedata,psd,savefolder,binsize = binsize,pulsetriggertime = pulsetriggertime,dt = 1/samplefreq, templatetime = templatetime,Format=Plot_Format)

    #use the wiener filter to generate the pulse statistics
    pulseheights = spp.GenPulseStatisticsHDF(res,f,wifilterphase,savefolder,IQCaldata,binsize = binsize,t_offset = t_offset,calibrate_drift = True,pulsetype = 'phase',plotbin = 0.2,Format=Plot_Format)

    #estimate the energy resolution
    spp.EnergyResolution(pulseheights,savefolder,photonum = 6,Format=Plot_Format)



