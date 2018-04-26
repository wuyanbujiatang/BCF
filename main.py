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
import random
import mvdr
if __name__ == '__main__':
    N = 10000#总采样点数
    m_Sound_1st = soundsource.Sound(1,N,90*np.pi/180,60*np.pi/180,0,0)#声源1
    t1,signal1,alpha1,sita1,c = m_Sound_1st.generate()
    m_Sound_2st = soundsource.Sound(1,N,105*np.pi/180,60*np.pi/180,0,0)#声源2
    t2,signal2,alpha2,sita2,c = m_Sound_2st.generate()
#    show.show_time_result(t1,signal1)
#    show.show_time_result(t2,signal2)
    
    m_Array = ascarr.Array([0,0,0])#声阵列
    m_Array.add_coors([[-0.3,0,0],[-0.15,0,0],[0.15,0,0],[0.3,0,0]])#添加阵元
    m_Array.add_coors([[-0.5,0,0],[-0.45,0,0],[0.45,0,0],[0.5,0,0]])#
    m_Array.add_coors([[0,0,-0.3],[0,0,-0.15],[0,0,0.15],[0,0,0.3]])#
    m_Array.add_coors([[0,0,-0.5],[0,0,-0.45],[0,0,0.45],[0,0,0.5]])#
#    B = np.array(m_Array.get_H(342,2*np.pi*214))
#    alha = list(B[:,1])
#    sita = list(B[:,2])
#    result = list(B[:,0])
#    show.show_3D_result(alpha,sita,result)
    
    down_fs = 10000#重采样率
    t,sound1 = m_Array.get_response_v2(t1,signal1,alpha1,sita1,c,down_fs)#阵列接收的声源1信号
    t,sound2 = m_Array.get_response_v2(t2,signal2,alpha2,sita2,c,down_fs)#阵列接收的声源2信号
    M = len(m_Array.get_coors())
    sigma = 0.001
    sound3 = np.array([random.gauss(0,sigma) for i in range(N*M)]).reshape(N,M)#全向白噪声
    sound = sound1 + sound2 + sound3
    show.show_all_received(t,sound)

    m_MVDR = mvdr.MVDR(t,sound,m_Array.get_coors())#MVDR声源定位
    orientation_result = m_MVDR.get_orientation_v2()
    result = list(orientation_result[:,0])
    alpha = list(orientation_result[:,1])
    sita = list(orientation_result[:,2])
    result = list(result/max(result))
    show.show_3D_result(alpha,sita,result)
    pos_index = result.index(max(result))
    print('alpha = ',alpha[pos_index])
    print('sita = ',sita[pos_index])