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
#from matplotlib import rc
#
#rc('text',usetex=True)
#rc('font',family='serif')

"Variable Initialization"
rawData=[]
avData=[]

"Paths to the data"
path_coordinates='C:\\Users\\uqfegger\\Documents\\Kent_powerDistrib\\_shakerDistribution.csv' #Path to csv file containing the coordinates
path_data_dirs='C:\\Users\\uqfegger\\Documents\\Kent_powerDistrib\\Batch\\' #Path to the directory containing the data directories

"Read Coordinates and create the grid for interpolation"
coordinates=genfromtxt(path_coordinates,skip_header=0,usecols=(1,2),delimiter=',') 
grid_width, grid_height = np.mgrid[0:max(coordinates[:,0]):1, 0:max(coordinates[:,1]):1] #dimensioned grid [mm]

"Create length to iterate over data"
len_dat=len(coordinates)

"Initialize integrated Irradiance"
intWatts=np.zeros((len_dat,1))

"Read data directory and sort the integers"
data=os.listdir(path_data_dirs) 
data = list(map(int, data))
data = sorted(data,key=int)

"Read the wavelength spectrum and calculate the step between wavelength reads"
spectrum=genfromtxt(path_data_dirs+'\\1\\1.IRR',skip_header=2,skip_footer=1,usecols=0)
dx=spectrum[1,]-spectrum[0,]

"Create length of spectrum to iterate over data"
len_spec=len(spectrum)

"Extract data from the different reads, average them and integrate the are under the curve of the averaged spectrum"
for i in data:
    probe=np.empty((len_spec,5))
    for j in range(0,5):
        probe[:,j]=genfromtxt(path_data_dirs+str(i)+'\\'+str(j+1)+'.IRR',skip_header=2,skip_footer=1,usecols=1)
    rawData.append(probe)
for k in range(0,len_dat):
    av=np.empty((len_spec,1))
    for l in range(0,len_spec):
        av[l,]=np.average(rawData[k][l,:])
    avData.append(av)
for m in range(0,len_dat):
    intWatts[m,0]=np.trapz(avData[m][:,0],dx=dx,axis=0)

"Associate the coordinates with their integrated Irradiance reading"
coordsWatts=np.empty((len_dat,3))
coordsWatts[:,0]=coordinates[:,0]
coordsWatts[:,1]=coordinates[:,1]
coordsWatts[:,[2]]=intWatts

"Interpolate the Irradiance data on the grid"
watts= griddata((coordsWatts[:,0],coordsWatts[:,1]),coordsWatts[:,2],(grid_width,grid_height),method='cubic')

"Setting up the plots:"
fig=plt.figure(1, (13.,7.))
axGrid=plt.subplot(111)
grid = ImageGrid(fig, 111,
            nrows_ncols = (1, 1),
            add_all=True,
            axes_pad=0.0,
            label_mode="L",
            cbar_mode="each",
            cbar_location="top",
            cbar_pad=0.05
            )

ax1=grid[0]
ax1.set_rasterization_zorder(0)
v = np.linspace(0, max(intWatts), 10, endpoint=True)
Cof=ax1.pcolormesh(grid_width, grid_height, watts,vmin=0.,vmax=max(intWatts))
Cof.set_rasterized(True)
ax1.set_xlabel("x [mm]", labelpad=18)
ax1.set_ylabel("y [mm]", labelpad=18)
plt.setp(axGrid, frame_on=False, xticks=(), yticks=())
grid.cbar_axes[0].colorbar(Cof,ticks=v)
grid.cbar_axes[0].set_xlabel("Irradiance [W m^{-2}]")

plt.savefig('powerDistribution.pdf', format='pdf')

fig2=plt.figure(2, (13.,7.))
for i in range(0,len_dat):
    plt.plot(spectrum,avData[i][:,0],label=str(i))
#    plt.legend()
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Irradiance Density [W m^{-2} nm^{-1}]')
    plt.savefig('spec.pdf',format='pdf')
