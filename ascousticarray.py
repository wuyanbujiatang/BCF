# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 20:02:52 2018

@author: wsj
"""
import numpy as np
class Array(object):
    def __init__(self,*coor):
        self.__coors = []
        for i in coor:
            self.__coors.append(i)
    def add_coors(self,coors):
        for coor in coors:
            self.__coors.append(coor)
    def get_coors(self):
        return self.__coors
    def get_H(self,c,w):
        sita_N = 100
        alpha_N = 100
        B = []
        for sita in range(sita_N):
            sita = sita*np.pi/sita_N
            for alpha in range(alpha_N):
                alpha = alpha*np.pi/alpha_N
                bf = 0 + 0.j
                for coor in self.__coors:
                    d = coor[0]*np.sin(sita)*np.cos(alpha)+coor[1]*np.sin(sita)*np.sin(alpha)+coor[2]*np.cos(sita)
                    v = w/c*d
                    bf = bf + complex(np.cos(v),-np.sin(v))/len(self.__coors)
                B.append([abs(bf),alpha,sita])
        return B
    def get_response(self,t,signal,alpha,sita,c,down_fs):
#        max_shift = 0
        sound = []
        for coor in self.__coors:
            d = coor[0]*np.sin(sita)*np.cos(alpha)+coor[1]*np.sin(sita)*np.sin(alpha)+coor[2]*np.cos(sita)
            dn = int(round(d/c/(t[1]-t[0])))
#            print(d/c/(t[1]-t[0]))
#            if max_shift<dn:
#                max_shift = dn
            if dn>0:
                plus_elements = np.zeros((dn,1))
                componnent = np.vstack((plus_elements,signal))
                componnent = componnent[0:len(t)]
            elif dn < 0:
                plus_elements = np.zeros((-dn,1))
                componnent = signal[-dn:]
                componnent = np.vstack((componnent,plus_elements))  
            else:
                componnent = signal
            if len(sound)==0:
                sound = componnent
            else:
#                print(np.shape(sound))
#                print(np.shape(componnent))
                sound = np.hstack((sound,componnent))
        down_dn = int(round(1/(t[1]-t[0])/down_fs))
        t = t[::down_dn]
        sound = sound[::down_dn]
        return t,sound