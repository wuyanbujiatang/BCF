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
        alpha_N = 50
        sita_N = 50
        alpha_arr = np.linspace(0,np.pi,num=alpha_N)
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
        alpha_N = 20
        sita_N = 20
        alpha_arr = np.linspace(0,np.pi,num=alpha_N)
        sita_arr = np.linspace(0,np.pi,num=sita_N)
        fusai = d/self.__c/(self.__t[1]-self.__t[0])
        result = []
        for sita in sita_arr:
            sin_sita = np.sin(sita)
            cos_sita = np.cos(sita)
            for alpha in alpha_arr:
                cos_alpha = np.cos(alpha)
                tao = [0]
                tao.append(-2*fusai*sin_sita*cos_alpha)
                tao.append(-fusai*sin_sita*cos_alpha)
                tao.append(fusai*sin_sita*cos_alpha)
                tao.append(2*fusai*sin_sita*cos_alpha)
                tao.append(-2*fusai*cos_sita)
                tao.append(-fusai*cos_sita)
                tao.append(fusai*cos_sita)
                tao.append(2*fusai*cos_sita)
                compound = np.zeros((len(self.__t),1))
                for m in range(len(self.__acoustic_array)):
                    dn = int(round(tao[m]))
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
    def get_cross_orientation_v2(self,d):
        alpha_N = 20
        sita_N = 20
        alpha_arr = np.linspace(0,np.pi,num=alpha_N)
        sita_arr = np.linspace(0,np.pi,num=sita_N)
        fusai = d/self.__c/(self.__t[1]-self.__t[0])
        result = []
        for sita in sita_arr:
            sin_sita = np.sin(sita)
            cos_sita = np.cos(sita)
            for alpha in alpha_arr:
                cos_alpha = np.cos(alpha)
                tao = [0]
                tao.append(-2*fusai*sin_sita*cos_alpha)
                tao.append(-fusai*sin_sita*cos_alpha)
                tao.append(fusai*sin_sita*cos_alpha)
                tao.append(2*fusai*sin_sita*cos_alpha)
                tao.append(-2*fusai*cos_sita)
                tao.append(-fusai*cos_sita)
                tao.append(fusai*cos_sita)
                tao.append(2*fusai*cos_sita)
                compound = np.zeros((len(self.__t),1))
                for m in range(len(self.__acoustic_array)):
                    dn = int(round(tao[m]))
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
        orientation_result = np.array(result)
        row,column = np.shape(orientation_result)
        alpha_arr = list(orientation_result[:,1])
        sita_arr = list(orientation_result[:,2])
        result = list(orientation_result[:,0])
        pos_index = result.index(max(result))
        get_sita = sita_arr[pos_index]
        get_alpha = alpha_arr[pos_index]
        alpha_N = 10
        sita_N = 10
        alpha_arr = np.linspace(get_alpha-np.pi/20,get_alpha+np.pi/20,num=alpha_N)
        sita_arr = np.linspace(get_sita-np.pi/20,get_sita+np.pi/20,num=sita_N)
        fusai = d/self.__c/(self.__t[1]-self.__t[0])
        result = []
        for sita in sita_arr:
            sin_sita = np.sin(sita)
            cos_sita = np.cos(sita)
            for alpha in alpha_arr:
                cos_alpha = np.cos(alpha)
                tao = [0]
                tao.append(-2*fusai*sin_sita*cos_alpha)
                tao.append(-fusai*sin_sita*cos_alpha)
                tao.append(fusai*sin_sita*cos_alpha)
                tao.append(2*fusai*sin_sita*cos_alpha)
                tao.append(-2*fusai*cos_sita)
                tao.append(-fusai*cos_sita)
                tao.append(fusai*cos_sita)
                tao.append(2*fusai*cos_sita)
                compound = np.zeros((len(self.__t),1))
                for m in range(len(self.__acoustic_array)):
                    dn = int(round(tao[m]))
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