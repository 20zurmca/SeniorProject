# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 21:00:45 2019

@author: zurmu
"""
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz #used for text matching

#importing data
roster_data = pd.read_csv("roster_data.csv")
starter_data = pd.read_csv("starter_data.csv")
accolade_data = pd.read_csv("accolades.csv")


roster_data.replace("NA", np.nan)
starter_data.replace("NA", np.nan)
accolade_data.replace("NA", np.nan)

roster_data.sort_values(by=["First_Name", "Last_Name"], ascending = [1, 1], inplace=True)

#%%
def match_names_roster_starter():
    """
    Method that makes sure the names in starter_data are formatted like in roster_data
    Needs optmization
    """
    class Match():
        def __init__(self, str1, str2, score):
            self.str1 = str1
            self.str2 = str2
            self.score = score
        
        def __gt__(self, other):
            return self.score > other.score
        
        def __str__(self):
            return str((self.str1, self.str2, self.score))
            
    def ratio(str1, str2):
        return fuzz.ratio(str1, str2)
    
    matches = []
    
    fuzz_score = 0
    for index1, row_a in roster_data.iterrows():
        name_from_roster_data = row_a["First_Name"] + " " + str(row_a["Last_Name"])
        for index2, row_b in starter_data.iterrows():
            #print(row_b["First_Name"], row_b["Last_Name"])
            name_from_starter_data = row_b["First_Name"] + " " + str(row_b["Last_Name"])
            fuzz_score = ratio(name_from_roster_data, name_from_starter_data)
            if fuzz_score < 100 and fuzz_score > 79:
                print("Potential match found:", (index1, index2), (name_from_roster_data, name_from_starter_data),
                      "with fuzz score:", fuzz_score)
                matches.append(Match(name_from_roster_data, name_from_starter_data, fuzz_score))    
            fuzz_score = 0
    
    with open('matching_names_roster_starter.txt', 'a') as f:
        for match in matches:
            f.write(str(match) + "\n")

#%%
def match_names_roster_conference():
    """
    Method that makes sure the names in accolade_data are formatted like in roster_data
    Needs optmization
    """
    class Match():
        def __init__(self, str1, str2, score):
            self.str1 = str1
            self.str2 = str2
            self.score = score
        
        def __gt__(self, other):
            return self.score > other.score
        
        def __str__(self):
            return str((self.str1, self.str2, self.score))
            
    def ratio(str1, str2):
        return fuzz.ratio(str1, str2)
    
    matches = []
    
    fuzz_score = 0
    for index1, row_a in roster_data.iterrows():
        name_from_roster_data = row_a["First_Name"] + " " + str(row_a["Last_Name"])
        for index2, row_b in accolade_data.iterrows():
            #print(row_b["First_Name"], row_b["Last_Name"])
            name_from_accolade_data = row_b["First_Name"] + " " + str(row_b["Last_Name"])
            fuzz_score = ratio(name_from_roster_data, name_from_accolade_data)
            if fuzz_score < 100 and fuzz_score > 79:
                print("Potential match found:", (index1, index2), (name_from_roster_data, name_from_accolade_data),
                      "with fuzz score:", fuzz_score)
                matches.append(Match(name_from_roster_data, name_from_accolade_data, fuzz_score))    
            fuzz_score = 0
    
    with open('matching_names_roster_accolade.txt', 'a') as f:
        for match in matches:
            f.write(str(match) + "\n")
            
               
    