# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 20:00:15 2018

@author: wsj
"""
import math
import random
import numpy as np
class Sound(object):
    def __init__(self,sigma,N,alpha,sita,amp,*f_set):
        self.__sigma = sigma
        self.__N = N
        self.__f_set = f_set
        self.__sita = sita
        self.__alpha = alpha
        self.__amp = amp
        self.__sigma = sigma
        self.__fs = 1e6
        self.__c = 342
    def generate(self):
        t = np.linspace(0,self.__N/self.__fs,num=self.__N)
        signal = np.zeros((self.__N,1))
        for f in self.__f_set:
            rad = [2*math.pi*f*n/self.__fs for n in range(self.__N)]
            component = np.array([self.__amp*math.sin(i) for i in rad]).reshape(self.__N,1)
            signal  = signal + component
        noise = np.array([random.gauss(0,self.__sigma) for i in range(self.__N)]).reshape(self.__N,1)
        signal = signal + noise
        return t,signal,self.__alpha,self.__sita,self.__c