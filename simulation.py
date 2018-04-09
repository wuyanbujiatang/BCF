# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 08:32:35 2018

@author: wsj
"""
import numpy as np
#import show
import soundsource
import ascousticarray as ascarr
#import beamforming as cbf
import cbfpso
import math
if __name__ == '__main__':
    
    f = 100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,855
    amp = 1
    down_fs = 20000
    gama = 0.01*4
    sita_N = 5
    alpha_N = 10
    error_sita = np.zeros((sita_N,alpha_N))
    error_alpha = np.zeros((sita_N,alpha_N))
    for sita_i in range(sita_N):
        sita = sita_i*np.pi/2/sita_N+0.1
        for alpha_i in range(alpha_N):
            
            alpha = alpha_i*2*np.pi/alpha_N
            m_Sound_1st = soundsource.Sound(gama,10000,alpha,sita,amp,*f)
            t1,signal1,alpha1,sita1,c = m_Sound_1st.generate()
            
            m_Array = ascarr.Array([0,0,0])
            m_Array.add_coors([[-0.4,0,0],[-0.2,0,0],[0.2,0,0],[0.4,0,0]])
            m_Array.add_coors([[0,-0.4,0],[0,-0.2,0],[0,0.2,0],[0,0.4,0]])
            
            t,sound1 = m_Array.get_response(t1,signal1,alpha1,sita1,c,down_fs)
            sound = sound1
            
            pso = cbfpso.PSO(20,50,t,sound,0.2)  
            pg = pso.evolve()
            get_sita = pg[0]
            get_alpha = pg[1]
            error_s = abs(get_sita-sita)
            error_a = abs(get_alpha-alpha)
            error_sita[sita_i,alpha_i] = error_s
            error_alpha[sita_i,alpha_i] = error_a
    print(10*math.log(0.707/gama/gama))
    print(np.mean(error_sita))
    print(np.mean(error_alpha))
            
