#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 20:19:08 2018
@author: wsj

"""
import numpy as np
import copy

class CBF(object):
    def __init__(self,t,sound,acoustic_array):
        self.__t = t
        self.__sound = sound
        self.__acoustic_array = acoustic_array
        self.__c = 342
    def get_orientation(self):
        alpha_N = 100
        sita_N = 100
        alpha_arr = np.linspace(0,2*np.pi,num=alpha_N)
        sita_arr = np.linspace(0,np.pi,num=sita_N)
        result = []
        for sita in sita_arr:
            for alpha in alpha_arr:
                m = 0
                compound = np.zeros((len(self.__t),1))
                for coor in self.__acoustic_array:
                    d = coor[0]*np.sin(sita)*np.cos(alpha)+coor[1]*np.sin(sita)*np.sin(alpha)+coor[2]*np.cos(sita)
                    dn = int(round(d/self.__c/(self.__t[1]-self.__t[0])))
                    if dn>0:
                        plus_elements = np.zeros((dn,1))
                        signal = copy.copy(self.__sound[:,m]).reshape(len(self.__t),1)
                        componnent = signal[dn:]
                        componnent = np.vstack((componnent,plus_elements))
                    elif dn < 0:
                        plus_elements = np.zeros((-dn,1))
                        signal = copy.copy(self.__sound[:,m]).reshape(len(self.__t),1)
                        componnent = np.vstack((plus_elements,signal))
                        componnent = componnent[0:len(self.__t)]
                    else:
                        signal = copy.copy(self.__sound[:,m]).reshape(len(self.__t),1)
                        componnent = signal
                    m = m + 1
                    compound = compound + componnent
                result.append([sum([abs(cell) for cell in compound]),alpha,sita])
        return result
    def get_cross_orientation(self,d):
        alpha_N = 40
        sita_N = 10
        alpha_arr = np.linspace(0,2*np.pi,num=alpha_N)
        sita_arr = np.linspace(0,np.pi,num=sita_N)
        result = []
        for sita in sita_arr:
            fusai = np.sin(sita)*d/self.__c
            for alpha in alpha_arr:
                sin_alpha = np.sin(alpha)
                cos_alpha = np.cos(alpha)
                tao = [0]
                tao.append(-2*fusai*cos_alpha)
                tao.append(-fusai*cos_alpha)
                tao.append(fusai*cos_alpha)
                tao.append(2*fusai*cos_alpha)
                tao.append(-2*fusai*sin_alpha)
                tao.append(-fusai*sin_alpha)
                tao.append(fusai*sin_alpha)
                tao.append(2*fusai*sin_alpha)
                compound = np.zeros((len(self.__t),1))
                for m in range(len(self.__acoustic_array)):
                    dn = int(round(tao[m]/(self.__t[1]-self.__t[0])))
                    if dn>0:
                        plus_elements = np.zeros((dn,1))
                        signal = copy.copy(self.__sound[:,m]).reshape(len(self.__t),1)
                        componnent = signal[dn:]
                        componnent = np.vstack((componnent,plus_elements))
                    elif dn < 0:
                        plus_elements = np.zeros((-dn,1))
                        signal = copy.copy(self.__sound[:,m]).reshape(len(self.__t),1)
                        componnent = np.vstack((plus_elements,signal))
                        componnent = componnent[0:len(self.__t)]
                    else:
                        signal = copy.copy(self.__sound[:,m]).reshape(len(self.__t),1)
                        componnent = signal
                    compound = compound + componnent
                result.append([sum([abs(cell) for cell in compound]),alpha,sita])
        return result
