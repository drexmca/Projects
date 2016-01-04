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
            FFT = np.abs(self.dft)
            FFT /= len(self.wave)
            FFT *= self.rate
            plt.plot(FFT)
            plt.show()
        else:
            x = np.linspace(0,len(self.wave)/float(self.rate), len(self.wave))
            plt.plot(x,self.wave)
            plt.show()

    def write_file(self, filename):
        sample = self.wave*32767./np.amax(np.abs(self.wave))
        sample = np.int16(sample)
        wavfile.write(filename, self.rate, sample)

    def __add__(self, other):
        new_wave = self.wave+other.wave 
        sum_obj = Signal(self.rate, new_wave)
        return sum_obj

    def calculate_DFT(self):
        self.dft = np.fft.fft(self.wave)
        


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
    A = generate_note(440,.25)
    C = generate_note(532.25,.25)
    E = generate_note(659.25,.25)
    B = generate_note(493.88,.25)
    D = generate_note(587.33,.25)
    D1 = generate_note(587.33,.5)
    F = generate_note(698.46,.25)
    G = generate_note(783.99,.25)
    G1 = generate_note(783.99,.5)
    E1 = generate_note(659.25,.5)
    ACE = A+C+E
    CEG = C+E+G
    ACE.write_file('chord1.wav')
    CEG.write_file('chordCEG.wav')
    chord_p = np.append(ACE.wave, CEG.wave)
    chord_p = Signal(44100., chord_p)
    chord_p.write_file('chords.wav')
    mary = np.append(E.wave,D.wave)
    mary = np.concatenate([E.wave, D.wave, C.wave,D.wave,E.wave,E.wave, E1.wave, D.wave, D.wave, D1.wave, E.wave, G.wave, G1.wave, E.wave, D.wave, C.wave, D.wave, E.wave, E.wave, E.wave, E.wave, D.wave, D.wave, E.wave, D.wave, C.wave],axis = 0)
    mary = Signal(44100.,mary)
    mary.write_file('chord2.wav')
    pass
generate_chord()
