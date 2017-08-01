# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 13:01:21 2017

@author: uqfegger
"""

import numpy as np
import os.path
from scipy.interpolate import griddata
from numpy import genfromtxt
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib import rc

rc('text',usetex = True)
rc('font',family = 'serif')

height = np.array([60,98,79]) #in mm
width = np.array([78,110,179,265,307,352,390]) #in mm
points_x,points_y = np.meshgrid(height,width,sparse = False, indexing = 'ij')

data = os.listdir("/PATH/TO/DATA/data.csv")
grid_width, grid_height  =  np.mgrid[78:390:1, 60:98:1] #dimensioned grid [mm]
data  =  list(map(int, data))
data  =  sorted(data,key = int)

spectrum  =  genfromtxt("/PATH/TO/DATA/data.csv",skip_header = 2,skip_footer = 1,usecols = 0)
sumWatts  =  np.empty((21,1))
rawData = []
avData = []
for i in data:
    probe = np.empty((250,5))
    av = np.empty((250,1))
    for j in range(0,5):   
        probe[:,j] = genfromtxt("H:\\02_Projects\\02_PPB-GRO-Batch\\04_Experiments\\01_IrradianceMeasurment\\data\\"+str(i)+'\\'+str(j+1)+'.IRR',skip_header = 2,skip_footer = 1,usecols = 1)
        rawData.append(probe)
    for k in range(0,250):
        av[k] = np.average(probe[k,:])
        avData.append(av)
        sumTemp = np.sum(av)
        sumWatts[i] = sumTemp #W/m^2
gridWatts = np.zeros((3,7))
for l in range(0,7):
    gridWatts[:,[l]] = sumWatts[(l*3):((l*3)+3)]
coordsWatts = np.empty((21,3))
for m in range(0,7):
    coordsWatts[m*3:(m*3)+3,0] = width[m]
    coordsWatts[m*3:(m*3)+3,1] = height[0:3]
    coordsWatts[:,[2]] = sumWatts
watts =  griddata((coordsWatts[:,0],coordsWatts[:,1]),sumWatts[:,0],(grid_width,grid_height),method = 'cubic')

fig = plt.figure(1, (13.,7.))
axGrid = plt.subplot(111)
grid  =  ImageGrid(fig, 111,
            nrows_ncols  =  (1, 1),
            add_all = True,
            axes_pad = 0.0,
            label_mode = "L",
            cbar_mode = "each",
            cbar_location = "top",
            cbar_pad = 0.05
            )

ax1 = grid[0]
ax1.set_rasterization_zorder(0)
v  =  np.linspace(0, max(sumWatts), 10, endpoint = True)
Cof = ax1.pcolormesh(grid_width, grid_height, watts,vmin = 0.,vmax = max(sumWatts))
Cof.set_rasterized(True)
ax1.set_xlabel("x [mm]", labelpad = 18)
ax1.set_ylabel("y [mm]", labelpad = 18)
plt.setp(axGrid, frame_on = False, xticks = (), yticks = ())
grid.cbar_axes[0].colorbar(Cof,ticks = v)
grid.cbar_axes[0].set_xlabel("Irradiance [W m^{-2}]")

plt.savefig('powerDistribution.pdf', format = 'pdf')
