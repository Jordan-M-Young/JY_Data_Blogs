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

l = lf_hitting.loc[:,'batting_avg']
l_std = round(l.std(),3)
l_mean = round(l.mean(),3)

r = rf_hitting.loc[:,'batting_avg']
r_std = round(r.std(),3)
r_mean = round(r.mean(),3)

s = s_hitting.loc[:,'batting_avg']
s_std = round(s.std(),3)
s_mean = round(s.mean(),3)


fig, axs = plt.subplots(3, 1)

axs[0].grid(zorder=0)
axs[0].hist(lf_hitting.loc[:,'batting_avg'],bins=20,color=vir_v,edgecolor='black',zorder=3)
axs[0].set_xlim([0,0.4])
axs[0].set_ylim([0,30])
axs[0].set_axisbelow(True)
axs[0].legend('L')
# axs[0].set_title('Left Handers')

fig.text(0.17, 0.8, 
         '$\sigma$ = ' + str(l_std) + '\n\nMean = ' + str(l_mean), 
         bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10},zorder=4)


axs[1].grid(zorder=0)
axs[1].hist(rf_hitting.loc[:,'batting_avg'],bins=20,color=vir_g,edgecolor='black',zorder=3)
axs[1].set_xlim([0,0.4])
axs[1].set_axisbelow(True)
# axs[1].set_title('Right Handers')
axs[1].legend('R')

fig.text(0.17, 0.527, 
         '$\sigma$ = ' + str(r_std) + '\n\nMean = ' + str(r_mean), 
         bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10},zorder=4)


axs[2].grid(zorder=0)
axs[2].hist(s_hitting.loc[:,'batting_avg'],bins=20,color=vir_y,edgecolor='black',zorder=3)
axs[2].set_xlim([0,0.4])
axs[2].legend('S')


fig.text(0.17, 0.255, 
         '$\sigma$ = ' + str(s_std) + '\n\nMean = ' + str(s_mean), 
         bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10},zorder=4)

                 
fig.text(0.06, 0.5, 'Players', ha='center', va='center', rotation='vertical')
fig.text(0.5, 0.03, 'Batting Average', ha='center', va='center')


plt.rc('axes', axisbelow=True)

