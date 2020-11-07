# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:18:47 2020

@author: jmyou
"""


import csv
import pandas as pd

def open_batter_file(filename):
    """basic csv opening function, opens up a file and places the data into a 
    'batters' list
    """
    with open(filename,'r',encoding='utf8') as csv_file:
        reader = csv.reader(csv_file,delimiter=',')
        batters = [row for row in reader]
    
    return batters

def get_stats(stat_file):
    """opens up the downloaded statistics file from baseballsavant
    """
    stats = open_batter_file(stat_file)
    stat_headers = stats.pop(0)
    stat_headers.append('Bat_Hand')
    stats.sort()
    stats.reverse()
    for s in stats:
        s[0] = s[0].replace(' ','')
        s[1] = s[1].replace(' ','')
    
    
    return stats,stat_headers

def single_switch_split(bts):
    """takes in a list of batters and separates them based on wheteher
    the batter in question is a single side hitter or a switch hitter
    """
    
    batters = []
    s_bts = []
    for i in range(len(bts)):
        if i == len(bts) - 1:
            continue
        elif i == 0:
            continue
        else:
            if (bts[i][0] == bts[i+1][0]) and bts[i][1] == bts[i+1][1]:
                s_bts.append(bts[i])
                continue
            elif (bts[i][0] == bts[i-1][0]) and bts[i][1] == bts[i-1][1]:
                continue
            else:
                batters.append(bts[i])
    
    return batters,s_bts

def right_left_split(batters):
    """splits a batters list into a right hander list and a left hander list
    """
    
    rh_bts = []
    lh_bts = []
    
    for b in batters:
        if b[2] == 'R':
            rh_bts.append(b)
        else:
            lh_bts.append(b)
    
    return rh_bts,lh_bts
    
def match_players(batters,stats):
    """Matches players between the batters list and the downloaded stat
    sheet from baseball savant or wherever else you might grab stats, then
    adds their batting hand to the main stat sheet
    """
    
    new_stats = []
    for i in range(len(batters)):
        for j in reversed(range(len(stats))):
            if batters[i][0] == stats[j][0]:
                if batters[i][1] == stats[j][1]:
                    # print(batters[i][0],batters[i][1],"------",stats[j][0],stats[j][1])
                    stats[j].append(batters[i][2])
                    new_stats.append(stats[j])
                    del(stats[j])
                else:
                    continue
            else:
                continue
    
    return new_stats

def format_data(bat_file,stat_file,rh_filename='Right_Hitter_player_attributes.csv',
                lh_filename='Left_Hitter_player_attributes.csv',
                switch_filename='Switch_Hitter_player_attributes.csv'):
    
    """opens the batter_side.csv file, formats the contained data,
    separates single side hitters from switch hitters, separates right
    handers from left handers, adds the hitting hand to the rest of the player
    statistics and writes three separate new stat .csv files based on hitting
    hand.
    """

    #opens raw batters file and writes data to list
    batters = open_batter_file(bat_file)
    
    #orders batters list by last name
    batters.sort()
    
    #formats raw data
    bts = []
    for i in range(len(batters)):
        
        b_name = batters[i][0].replace(' ','')
        batter = b_name.split(',')
        batter.append(batters[i][1])
        
        if len(batter) > 2:
            bts.append(batter)
    
    
    #separates switch hitters from single side hitters
    batters,s_bts = single_switch_split(bts)
    
    #separates right handers from left handers
    rh_bts,lh_bts = right_left_split(batters)
    
    #opens stat sheet
    stats,stat_headers = get_stats(stat_file)
    
        
    stat_dic = {rh_filename:rh_bts,lh_filename:lh_bts,switch_filename:s_bts}
    for key,value in stat_dic.items():
        new_stats = match_players(value,stats)
        new_stats = pd.DataFrame(new_stats,columns=stat_headers)
        print(new_stats)
        try:
            new_stats = new_stats.drop(labels='',axis=1)
            new_stats.to_csv(key,index=False)
        except KeyError:
            new_stats.to_csv(key,index=False)
        
  
        


#Runs the data cleaning routine!
bat_file = 'C:/Users/jmyou/Desktop/bb_data_project/Batter_Side.csv'
stat_file = 'C:/Users/jmyou/Desktop/bb_data_project/2020_MLB_player_attributes.csv'
format_data(bat_file,stat_file)





