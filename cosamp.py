# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 08:51:37 2018

@author: wsj
"""
import numpy as np
class CoSaMP(object):
    def __init__(self,t,sound,acoustic_array):
        self.__t = t
        self.__sound = sound
        self.__acoustic_array = acoustic_array
        self.__c = 342
        self.__fft_sound = np.array([[0j]*len(acoustic_array)]*(int(len(t)/2)))
        for m in range(len(acoustic_array)):
            self.__fft_sound[:,m] = (np.fft.fft(self.__sound[:,m])/len(t))[range(int(len(t)/2))]
    def get_orientation(self):
        return np.shape(self.__fft_sound)