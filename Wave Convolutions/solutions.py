# Name this file solutions.py.
"""Volume II Lab 10: Fourier II (Filtering and Convolution)
Donald Rex McArthur
Math 321
Nov...
"""
from scipy.io import wavfile
import numpy as np
import lab9
import scipy as sp
from matplotlib import pyplot as plt

# Problem 1: Implement this function.
def clean_signal(outfile='prob1.wav'):
    """Clean the 'Noisysignal2.wav' file. Plot the resulting sound
    wave and write the resulting sound to the specified outfile.
    """
    rate, data = wavfile.read('Noisysignal2.wav')
    jfk = lab9.Signal(rate, data)
    jfk.plot(True)
    fsig = sp.fft(data, axis = 0)
    for j in xrange(14500,50000):
        fsig[j]=0
        fsig[-j]=0
    newsig = sp.ifft(fsig)
    newsig = sp.real(newsig)
    newsig = sp.int16(newsig/sp.absolute(newsig).max()*32767)
    clear = lab9.Signal(rate,newsig)
    clear.write_file(outfile)
    clear.plot(True)
    pass
    
# Problem 3: Implement this function.
def convolve(source='chopin.wav', pulse='balloon.wav', outfile='prob3.wav'):
    """Convolve the specified source file with the specified pulse file, then
    write the resulting sound wave to the specified outfile.
    """
    rate, data = wavfile.read(source)
    rate_sample, data_sample = wavfile.read(pulse)
    ###Convert to Mono, gosh darn it this took forever to figure out.
    data = data[:,0]
    data_sample = data_sample[:,0]
    balancezeros = np.zeros(rate)
    data = np.append(data, balancezeros)
    newzeros = np.zeros((np.abs(len(data)-len(data_sample))))
    data_sample = np.append(data_sample,newzeros)
    fourier = np.fft.fft(data)
    fourier_sample = np.fft.fft(data_sample)
    ##This element-wise multiplies the two products
    conv = fourier*fourier_sample
    sig = np.real(sp.ifft(conv))
    sig = sp.int16(sig/sp.absolute(sig).max()*32767)
    wavfile.write(outfile,rate,sig)
    pass


# Problem 4: Implement this function.
def white_noise(outfile='prob4.wav'):
    """Generate some white noise, write it to the specified outfile,
    and plot the spectrum (DFT) of the signal.
    """
    samplerate = 44100
    w_noise = sp.int16(sp.random.randint(-32767,32767, samplerate*10.))
    spectrum = sp.fft(w_noise)
    wavfile.write(outfile,samplerate,w_noise)
    frequency = samplerate*(np.arange(1,len(spectrum)+1,1)*1.)/len(w_noise)
    plt.plot(frequency, spectrum)
    plt.show()
    pass


