# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 12:55:07 2018

@author: wsj
"""

import numpy as np   
import copy  
import matplotlib.pyplot as plt  
class PSO(object):  
    def __init__(self, population_size, max_steps,t,sound,d):
        self.__t = t
        self.__sound = sound
        self.__d = d
        self.__c = 342
        
        self.w = [0.4,0.9]  # 惯性权重  
        self.c1 = self.c2 = 2  
        self.population_size = population_size  # 粒子群数量  
        self.dim = 2  # 搜索空间的维度  
        self.max_steps = max_steps  # 迭代次数  

        self.x0_bound = [0,np.pi/2]
        self.x1_bound = [0,2*np.pi]

        self.x = np.random.uniform(self.x0_bound[0], self.x0_bound[1],  
                                   (self.population_size, self.dim))  # 初始化粒子群位置
        self.x[:,1] = self.x1_bound[1]/self.x0_bound[1]*self.x[:,1] # 初始化粒子群位置
        preset_x = np.array([[0,0],[np.pi/8,0],[3*np.pi/8,0.01],[0,0.01],
                  [np.pi/4,0],[np.pi/4,np.pi/4],[np.pi/4,np.pi/2],[np.pi/4,3*np.pi/4],[np.pi/4,np.pi],[np.pi/4,5*np.pi/4],[np.pi/4,3*np.pi/2],[np.pi/4,7*np.pi/4],
                  [np.pi/2,0],[np.pi/2,np.pi/4],[np.pi/2,np.pi/2],[np.pi/2,3*np.pi/4],[np.pi/2,np.pi],[np.pi/2,5*np.pi/4],[np.pi/2,3*np.pi/2],[np.pi/2,7*np.pi/4]]).reshape(20,2)
        self.x[0:len(preset_x),:] = preset_x
        self.v0_bound = [-0.25,0.25]
        self.v1_bound = [-1,1]
        self.v = self.v0_bound[1]*(2*np.random.rand(self.population_size, self.dim)-1)  # 初始化粒子群速度
        self.v[:,1] = self.v1_bound[1]/self.v0_bound[1]*self.v[:,1] # 初始化粒子群速度
        
        fitness = self.calculate_fitness(self.x)  
        self.p = self.x  # 个体的最佳位置  
        self.pg = self.x[np.argmin(fitness)]  # 全局最佳位置  
        self.individual_best_fitness = fitness  # 个体的最优适应度  
        self.global_best_fitness = np.max(fitness)  # 全局最佳适应度
#        print(self.x)
  
    def calculate_fitness(self, x):
        result = []
        for i in range(self.population_size):
            sita = x[i,0]
            alpha = x[i,1]
            fusai = np.sin(sita)*self.__d/self.__c
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
            for m in range(len(tao)):
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
            result.append(sum([abs(cell) for cell in compound]))
        return np.array(result).reshape(self.population_size,1)  

    def evolve(self): 
        for step in range(self.max_steps):  
            r1 = np.random.rand(self.population_size, self.dim)  
            r2 = np.random.rand(self.population_size, self.dim)  
            # 更新速度和权重
            w = self.w[1] - (self.w[1]-self.w[0])/self.max_steps*step
            self.v = w*self.v+self.c1*r1*(self.p-self.x)+self.c2*r2*(self.pg-self.x)  
            self.x = self.v + self.x
            for i in range(self.population_size):
                if self.v[i,0]>self.v0_bound[1]:
                   self.v[i,0] = self.v0_bound[1]
                elif self.v[i,0]<self.v0_bound[0]:
                   self.v[i,0] = self.v0_bound[0]

                if self.v[i,1]>self.v1_bound[1]:
                   self.v[i,1] = self.v1_bound[1]
                elif self.v[i,1]<self.v1_bound[0]:
                   self.v[i,1] = self.v1_bound[0] 

                if self.x[i,0]>self.x0_bound[1]:
                   self.x[i,0] = self.x0_bound[1]
                elif self.x[i,0]<self.x0_bound[0]:
                   self.x[i,0] = self.x0_bound[0]

                if self.x[i,1]>self.x1_bound[1]:
                   self.x[i,1] = self.x1_bound[1]
                elif self.x[i,1]<self.x1_bound[0]:
                   self.x[i,1] = self.x1_bound[0]              
            fitness = self.calculate_fitness(self.x)  
            # 需要更新的个体  
            update_id = np.less(self.individual_best_fitness, fitness)
            self.p[update_id] = self.x[update_id]  
            self.individual_best_fitness[update_id] = fitness[update_id]  
            # 新一代出现了更小的fitness，所以更新全局最优fitness和位置  
            if np.max(fitness) > self.global_best_fitness:  
                self.pg = self.x[np.argmax(fitness)]  
                self.global_best_fitness = np.max(fitness)
#            print('best fitness: %.5f, mean fitness: %.5f' % (self.global_best_fitness, np.mean(fitness)))  
        return self.pg
  
#pso = PSO(40, 100)  
#pso.evolve()  