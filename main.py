#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 20:19:08 2018
@author: wsj
This is a time delay adding beamforming,is also named Conventional Beamforming(CBF).
Acoustic array structure is cross,as shown below.
                        y axis
                        ↑
                        *
                        *
                    * * * * * → x axis
                        *
                        *
"""
import numpy as np
import show
import soundsource
import ascousticarray as ascarr
#import beamforming as cbf
import cbfpso
if __name__ == '__main__':
    m_Sound_1st = soundsource.Sound(0.001,10000,np.pi,np.pi/4,1,500)
    t1,signal1,alpha1,sita1,c = m_Sound_1st.generate()
    m_Sound_2st = soundsource.Sound(0.01,10000,np.pi,0.5*np.pi/4,1,0,0)
    t2,signal2,alpha2,sita2,c = m_Sound_2st.generate()
    show.show_time_result(t1,signal1)
#    show.show_time_result(t2,signal2)
    
    m_Array = ascarr.Array([0,0,0])
    m_Array.add_coors([[-0.4,0,0],[-0.2,0,0],[0.2,0,0],[0.4,0,0]])
    m_Array.add_coors([[0,-0.4,0],[0,-0.2,0],[0,0.2,0],[0,0.4,0]])
    B = np.array(m_Array.get_H(342,5e2))
#    alpha = list(B[:,1])
#    sita = list(B[:,2])
#    result = list(B[:,0])
#    show.show_3D_result(alpha,sita,result)
    
    down_fs = 20000
    t,sound1 = m_Array.get_response(t1,signal1,alpha1,sita1,c,down_fs)
    t,sound2 = m_Array.get_response(t2,signal2,alpha2,sita2,c,down_fs)
    sound = sound1 + sound2
    show.show_all_received(t,sound)
    
    pso = cbfpso.PSO(20,100,t,sound,0.2)  
    pg = pso.evolve()
    print('alpha = ',pg[1])
    print('sita = ',pg[0])
#    m_CBF = cbf.CBF(t,sound,m_Array.get_coors())
##    orientation_result = np.array(m_CBF.get_orientation())
#    orientation_result = np.array(m_CBF.get_cross_orientation(0.2))
#    row,column = np.shape(orientation_result)
#    alpha = list(orientation_result[:,1][0:int(row/2)])
#    sita = list(orientation_result[:,2][0:int(row/2)])
#    result = list(orientation_result[:,0][0:int(row/2)])
#    show.show_result(result)
#    show.show_3D_result(alpha,sita,result)
#    pos_index = result.index(max(result))
#    print('alpha = ',alpha[pos_index])
#    print('sita = ',sita[pos_index])
    