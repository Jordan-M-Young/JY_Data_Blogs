# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:53:16 2020

@author: jmyou
"""


import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress as linreg
import numpy as np


#Opens player hitting statistics
lf_hitting = pd.read_csv('C:/Users/jmyou/Desktop/bb_data_project/Left_Hitter_basic_hitting_Stats.csv')
rf_hitting = pd.read_csv('C:/Users/jmyou/Desktop/bb_data_project/Right_Hitter_basic_hitting_Stats.csv')
s_hitting = pd.read_csv('C:/Users/jmyou/Desktop/bb_data_project/Switch_Hitter_basic_hitting_Stats.csv')


#Opens player running statistics
lf_running = pd.read_csv('C:/Users/jmyou/Desktop/bb_data_project/Left_Hitter_run_Stats.csv')
rf_running = pd.read_csv('C:/Users/jmyou/Desktop/bb_data_project/Right_Hitter_run_Stats.csv')
s_running = pd.read_csv('C:/Users/jmyou/Desktop/bb_data_project/Switch_Hitter_run_Stats.csv')

#Gets rid of NaN values, I did this so the following linear regressions would
#make sense.
lf_running = lf_running.dropna(axis=0)
rf_running = rf_running.dropna(axis=0)
s_running = s_running.dropna(axis=0)

#Linear regressions for each group of batters
l_reg = linreg(lf_running.loc[:,'sprint_speed'],lf_running.loc[:,'hp_to_1b'])
r_reg = linreg(rf_running.loc[:,'sprint_speed'],rf_running.loc[:,'hp_to_1b'])
s_reg = linreg(s_running.loc[:,'sprint_speed'],s_running.loc[:,'hp_to_1b'])



#Best fit lines of each group of hitters
x = np.array([i for i in range(20,35)])
yr = r_reg[0]*x + r_reg[1]
yl = l_reg[0]*x + l_reg[1]
ys = s_reg[0]*x + s_reg[1]

residual = yr - yl

#Viridis Colors
vir_v = (71/255, 33/255, 115/255) 
vir_b = (46/255, 111/255, 142/255)
vir_g = (40/255, 175/255, 126/255)
vir_y =  (188/255, 223/255, 37/255)

# l = lf_hitting.loc[:,'b_hit_ground'] / lf_hitting.loc[:,'b_out_ground']
# l_std = round(l.std(),3)
# l_mean = round(l.mean(),3)

# r = rf_hitting.loc[:,'b_hit_ground'] / rf_hitting.loc[:,'b_out_ground']
# r_std = round(r.std(),3)
# r_mean = round(r.mean(),3)

# s = s_hitting.loc[:,'b_hit_ground'] / s_hitting.loc[:,'b_out_ground']
# s_std = round(s.std(),3)
# s_mean = round(s.mean(),3)



# Plots best fit lines
plt.plot(x,yl,color=vir_v,zorder=3)
plt.plot(x,yr,color=vir_g,zorder=3)
plt.plot(x,ys,color=vir_y,zorder=3)


#Plots data from Baseball Savant
plt.scatter(lf_running.loc[:,'sprint_speed'],
            lf_running.loc[:,'hp_to_1b'],
            color=vir_v,edgecolors='black',s=60,zorder=4)

plt.scatter(rf_running.loc[:,'sprint_speed'],
            rf_running.loc[:,'hp_to_1b'],
            color=vir_g,edgecolors='black',s=60,zorder=4)

plt.scatter(s_running.loc[:,'sprint_speed'],
            s_running.loc[:,'hp_to_1b'],
            color=vir_y,edgecolors='black',s=60,zorder=4)

#Figure formatting
plt.xlim([23,31])
plt.ylim([3.8,5.2])

plt.xlabel('Runner Speed (ft/s)')
plt.ylabel('HP to 1B (s)')

plt.legend(['L | R$^2$ = ' + str(round(l_reg[2]**2,2)),
            'R | R$^2$ = ' + str(round(r_reg[2]**2,2)),
            'S | R$^2$ = ' + str(round(s_reg[2]**2,2))],
           framealpha=1)
plt.rc('axes', axisbelow=True)
plt.grid(zorder=0)
