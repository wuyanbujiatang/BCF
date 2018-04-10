# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 08:32:35 2018

@author: wsj
"""
import numpy as np
#import show
import soundsource
import ascousticarray as ascarr
import beamforming as cbf
import cbfpso
import math
if __name__ == '__main__':
    
#    f = 100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,855
    f=855
    amp = 1
    down_fs = 20000
    gama = 1
    sita_N = 9
    alpha_N = 9
    error_sita = np.zeros((sita_N,alpha_N))
    error_alpha = np.zeros((sita_N,alpha_N))
    for sita_i in range(sita_N):
        sita = sita_i*np.pi/sita_N+0.1
        for alpha_i in range(alpha_N):
            alpha = alpha_i*np.pi/alpha_N+0.1
            m_Sound_1st = soundsource.Sound(gama,10000,alpha,sita,amp,f)
            t1,signal1,alpha1,sita1,c = m_Sound_1st.generate()
            
            m_Array = ascarr.Array([0,0,0])
            m_Array.add_coors([[-0.4,0,0],[-0.2,0,0],[0.2,0,0],[0.4,0,0]])
            m_Array.add_coors([[0,0,-0.4],[0,0,-0.2],[0,0,0.2],[0,0,0.4]])
            
            t,sound1 = m_Array.get_response(t1,signal1,alpha1,sita1,c,down_fs)
            sound = sound1
            
#            pso = cbfpso.PSO(25,40,t,sound,0.2)  
#            pg = pso.evolve()
#            get_sita = pg[0]
#            get_alpha = pg[1]
            m_CBF = cbf.CBF(t,sound,m_Array.get_coors())
#            orientation_result = np.array(m_CBF.get_orientation())
            orientation_result = np.array(m_CBF.get_cross_orientation_v2(0.2))
            row,column = np.shape(orientation_result)
            alpha_arr = list(orientation_result[:,1])
            sita_arr = list(orientation_result[:,2])
            result = list(orientation_result[:,0])
            pos_index = result.index(max(result))
            get_sita = sita_arr[pos_index]
            get_alpha = alpha_arr[pos_index]
            error_s = abs(get_sita-sita)
            error_a = abs(get_alpha-alpha)
            error_sita[sita_i,alpha_i] = error_s
            error_alpha[sita_i,alpha_i] = error_a
    print(10*math.log(0.707/gama/gama))
    print(np.mean(error_sita))
    print(np.mean(error_alpha))
            
