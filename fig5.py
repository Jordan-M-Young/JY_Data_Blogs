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

l_attributes = pd.read_csv('C:/Users/jmyou/Desktop/bb_data_project/Left_Hitter_player_attributes.csv')
r_attributes = pd.read_csv('C:/Users/jmyou/Desktop/bb_data_project/Right_Hitter_player_attributes.csv')
s_attributes = pd.read_csv('C:/Users/jmyou/Desktop/bb_data_project/Switch_Hitter_player_attributes.csv')

lc = lf_running.columns
rc = rf_running.columns
sc = s_running.columns


#Linear regressions for each group of batters
l_reg = linreg(lf_running.loc[:,'sprint_speed'],lf_running.loc[:,'hp_to_1b'])
r_reg = linreg(rf_running.loc[:,'sprint_speed'],rf_running.loc[:,'hp_to_1b'])
s_reg = linreg(s_running.loc[:,'sprint_speed'],s_running.loc[:,'hp_to_1b'])



new_l = pd.merge(l_attributes,lf_running,
                 left_on=['nameLast','nameFirst']
                 ,right_on=['last_name', lc[1]])

new_r = pd.merge(r_attributes,rf_running,
                 left_on=['nameLast','nameFirst']
                 ,right_on=['last_name', rc[1]])

new_s = pd.merge(s_attributes,s_running,
                 left_on=['nameLast','nameFirst']
                 ,right_on=['last_name', sc[1]])

l_iT = new_l.loc[:,'sprint_speed']*l_reg[0] + l_reg[1]
r_iT = new_r.loc[:,'sprint_speed']*r_reg[0] + r_reg[1]
s_iT = new_s.loc[:,'sprint_speed']*s_reg[0] + s_reg[1]


l_dt = l_iT - new_l.loc[:,'hp_to_1b']
r_dt = r_iT - new_r.loc[:,'hp_to_1b']
s_dt = s_iT - new_s.loc[:,'hp_to_1b']

l_wt = (new_l.loc[:,'weight'] / 2.20462) / ((new_l.loc[:,'height'] / 39.3701)**2)
r_wt = (new_r.loc[:,'weight'] / 2.20462) / ((new_r.loc[:,'height'] / 39.3701)**2)
s_wt = (new_s.loc[:,'weight'] / 2.20462) / ((new_s.loc[:,'height'] / 39.3701)**2)

l_reg2 = linreg(l_dt,l_wt)
r_reg2 = linreg(r_dt,r_wt)
s_reg2 = linreg(s_dt,s_wt)

x = np.array([i/100 for i in range(-10,30)])
yr = r_reg2[0]*x + r_reg2[1]
yl = l_reg2[0]*x + l_reg2[1]
ys = s_reg2[0]*x + s_reg2[1]

#Viridis Colors
vir_v = (71/255, 33/255, 115/255) 
vir_b = (46/255, 111/255, 142/255)
vir_g = (40/255, 175/255, 126/255)
vir_y =  (188/255, 223/255, 37/255)



plt.scatter(l_dt,l_wt,color=vir_v,zorder=3,edgecolors='black',s=60)
plt.scatter(r_dt,r_wt,color=vir_g,zorder=3,edgecolors='black',s=60)
plt.scatter(s_dt,s_wt,color=vir_y,zorder=3,edgecolors='black',s=60)
plt.ylim([20,36])
plt.xlabel('Time Differential (seconds)')
plt.ylabel('BMI (kg/m$^2$)')
plt.legend(['L','R','S'])
plt.grid(zorder=0)
