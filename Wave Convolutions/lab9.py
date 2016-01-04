# name this file solutions.py
"""Volume II Lab 9: Discrete Fourier Transform
Donald Rex McArthur
Class 345

"""
import numpy as np
from scipy.io import wavfile
import os
from matplotlib import pyplot as plt

# Modify this class for problems 1, 2, 4, and 5.
class Signal(object):
    def __init__(self, rate, wave):
        self.rate = rate
        self.wave = wave

    def plot(self, dft=False):
        if dft:
            FFT = np.abs(np.fft.fft(self.wave))
            FFT /= len(self.wave)
            FFT *= self.rate
            plt.plot(FFT)
            plt.show()
        else:
            x = np.linspace(0,len(self.wave)/float(self.rate), len(self.wave))
            plt.plot(x,self.wave)
            plt.show()

    def write_file(self, filename):
        sample = self.wave*32767./np.amax(self.wave)
        sample = np.int16(sample)
        wavfile.write(filename, self.rate, sample)

def test1():
    rate, wave = wavfile.read('tada.wav')
    tada = Signal(rate, wave)
    return tada
#
#tada = test1()
#tada.plot(True)
#tada.plot(False)
#

# Problem 3: Implement this function.
def generate_note(frequency=440., duration=5., rate=44100.):
    """Return an instance of the Signal class corresponding to the desired
    soundwave. Sample at a rate of 44100 samples per second.
    """
    t = np.linspace(0,duration,rate*duration)
    wave = np.sin(2*np.pi*(frequency)*t)
    note = Signal(rate, wave) 
    return note
    
def test2():
    A = generate_note(440, 1)
    return A
#
#A = test2()
#A = Signal(44100,A)
#A.plot(True)
#
# Problem 4: Implement this function.
def DFT(samples):
    """Calculated the DFT of the given array of samples."""
    c = []
    for k in xrange(len(samples)):
        c_k = []
        for n in xrange(len(samples)):
            var = samples[n] * np.exp((-2*np.pi*1j*n*k)/float(len(samples)))
            c_k = np.append(c_k, var)
            c_k = np.sum(c_k)
        c.append(c_k)
    return c
# Problem 6: Implement this function.
def generate_chord():
    """Write a chord to a new file, 'chord1.wav'. Write a chord that changes
    over time to a new file, 'chord2.wav'.
    """
    A = generate_note(440,1)
    C = generate_note(532.25,1)
    E = generate_note(659.25,1)
    B = generate_note(493.88,1)
    D = generate_note(587.33,1)
    F = generate_note(698.46,1)
    G = generate_note(783.99,1)
    ACE = A.wave+C.wave+E.wave
    CEG = C.wave+E.wave+G.wave
    ACE = Signal(44100,ACE)
    CEG = Signal(44100,CEG)
    ACE.write_file('chord1')
    CEG.write_file('chordCEG')
    zeros = np.zeros(len(ACE.wave))
    mary = np.append(E.wave,D.wave)
    mary = np.append(mary,[C.wave,D.wave,E.wave,E.wave,E.wave,D.wave,D.wave,D.wave,E.wave,E.wave,E.wave])
    mary = Signal(44100,mary)
    mary.write_file('chord2')
    pass
