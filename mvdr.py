# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 20:33:38 2018
t,sound,acoustic_array分别为采样时间序列，阵列的输出声音信号，声阵列
@author: wsj
"""

import numpy as np
class MVDR(object):
    def __init__(self,t,sound,acoustic_array):
        self.__t = t
        self.__sound = sound
        self.__acoustic_array = acoustic_array
        self.__c = 342
        self.__Tn = 200
        self.__fft_sound = 0j*np.zeros((int(self.__Tn/2),len(acoustic_array)))
        self.__R = []
        for i in range(int(len(t)/self.__Tn)):
            for m in range(len(acoustic_array)):
                buff = self.__sound[i*self.__Tn:(i+1)*self.__Tn,m]
                self.__fft_sound[:,m] = (np.fft.fft(buff)/self.__Tn*2)[0:int(self.__Tn/2)]
            for j in range(int(self.__Tn/2)):
                if i==0:
                    self.__R.append(np.mat(self.__fft_sound[j,:]).H*np.mat(self.__fft_sound[j,:])/(int(len(t)/self.__Tn)))
                else: 
                    self.__R[j] = self.__R[j] + (np.mat(self.__fft_sound[j,:]).H*np.mat(self.__fft_sound[j,:])/(int(len(t)/self.__Tn)))
    def get_orientation(self):
        selected_fre = list(range(12,21))
        alpha_N = 180
        sita_N = 180
        alpha_arr = np.linspace(0,np.pi,num=alpha_N)
        sita_arr = np.linspace(0,np.pi,num=sita_N)
        p = []
        for sita in sita_arr:
            for alpha in alpha_arr:
                p_cell = 0
                for fre in selected_fre:
                    a = []
                    for coor in self.__acoustic_array:
                        d = coor[0]*np.sin(sita)*np.cos(alpha)+coor[1]*np.sin(sita)*np.sin(alpha)+coor[2]*np.cos(sita)
                        phase = 2*np.pi*fre/((self.__t[1]-self.__t[0])*self.__Tn)*d/self.__c
                        a.append(np.exp(-1j*phase))
                    a = np.mat(a)
                    p_cell = p_cell + 1/(a*np.mat(self.__R[fre]).I*a.H)
                p.append([abs(p_cell[0,0]),alpha/np.pi*180,sita/np.pi*180])
        p = np.array(p)
        return p
    def get_orientation_v2(self):
        selected_fre = list(range(12,21))       
        alpha_N = 20
        sita_N = 20
        alpha_arr = np.linspace(0,np.pi,num=alpha_N)
        sita_arr = np.linspace(0,np.pi,num=sita_N)
        p = []
        for sita in sita_arr:
            for alpha in alpha_arr:
                p_cell = 0
                for fre in selected_fre:
                    a = []
                    for coor in self.__acoustic_array:
                        d = coor[0]*np.sin(sita)*np.cos(alpha)+coor[1]*np.sin(sita)*np.sin(alpha)+coor[2]*np.cos(sita)
                        phase = 2*np.pi*fre/((self.__t[1]-self.__t[0])*self.__Tn)*d/self.__c
                        a.append(np.exp(-1j*phase))
                    a = np.mat(a)
                    p_cell = p_cell + a*np.mat(self.__R[fre])*a.H
                p.append(abs(p_cell[0,0]))
        pos_index = p.index(max(p))
        sita_like_pos = int(pos_index/alpha_N)
        alpha_like_pos = pos_index%alpha_N
        alpha_min = alpha_arr[alpha_like_pos] - alpha_arr[1] + alpha_arr[0]
        alpha_max = alpha_arr[alpha_like_pos] + alpha_arr[1] - alpha_arr[0]
        sita_min = sita_arr[sita_like_pos] - sita_arr[1] + sita_arr[0]
        sita_max = sita_arr[sita_like_pos] + sita_arr[1] - sita_arr[0]
        print(alpha_min,alpha_max,sita_min,sita_max)
        alpha_N = 10
        sita_N = 10
        alpha_arr = np.linspace(alpha_min,alpha_max,num=alpha_N)
        sita_arr = np.linspace(sita_min,sita_max,num=sita_N)
        p = []
        for sita in sita_arr:
            for alpha in alpha_arr:
                p_cell = 0
                for fre in selected_fre:
                    a = []
                    for coor in self.__acoustic_array:
                        d = coor[0]*np.sin(sita)*np.cos(alpha)+coor[1]*np.sin(sita)*np.sin(alpha)+coor[2]*np.cos(sita)
                        phase = 2*np.pi*fre/((self.__t[1]-self.__t[0])*self.__Tn)*d/self.__c
                        a.append(np.exp(-1j*phase))
                    a = np.mat(a)
                    p_cell = p_cell + 1/(a*np.mat(self.__R[fre]).I*a.H)
                p.append([abs(p_cell[0,0]),alpha/np.pi*180,sita/np.pi*180])
        p = np.array(p)
        return p