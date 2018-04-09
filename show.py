# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 17:17:26 2018

@author: wsj
"""
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D
def show_all_received(t,x):
    fig,axes = plt.subplots(nrows=1,ncols=1,figsize=(8,6)) 
    n,m = np.shape(x)
    total = np.zeros((n,1))
    for i in range(m):
        total = [(total[j]+x[j,i]) for j in range(n)]
        line1, = axes.plot(t,x[:,i],'b')
    total = [total[j]/m for j in range(n)]
    line2, = axes.plot(t,total,'r')
    axes.legend((line1,line2),('all received signal','synthesis signal'),loc = 'upper right')
    axes.set_xlabel(u'time(s)')
    axes.set_ylabel(u'signal(v)')
    axes.set_title('sound')
def show_3D_result(alpha,sita,result):
    fig=plt.figure(figsize=(8,6))
#    axes = fig.gca(projection='3d')
    axes=fig.add_subplot(111,projection='3d')
    axes.scatter(alpha,sita,result,s=1,c='r')
    axes.set_xlabel(u'alpha(rad)')
    axes.set_ylabel(u'sita(rad)')
    axes.set_zlabel(u'result')
    axes.set_title('sound pursuit result')
    plt.show()
    
def show_result(x):
    fig,axes = plt.subplots(nrows=1,ncols=1,figsize=(8,6)) 
    axes.plot(x,'b')
    axes.set_xlabel(u'dot')
    axes.set_ylabel(u'signal(v)')
    axes.set_title('sound')
    
def show_time_result(t,x):
    fig,axes = plt.subplots(nrows=1,ncols=1,figsize=(8,6)) 
    axes.plot(t,x,'b')
    axes.set_xlabel(u'time(s)')
    axes.set_ylabel(u'signal(v)')
    axes.set_title('sound')