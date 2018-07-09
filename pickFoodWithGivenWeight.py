# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
home = str(Path.home())
PATH = home + "\\Desktop\\ee_grad_project\\"

import os
os.chdir(PATH)

#my library
from foodDataWeightFromLogV2 import calWeightFromLog

OUTPUT = PATH +  "dataFile\\output_log.xlsx"
FOOD_DATA = PATH + "dataFile\\food_data.xlsx"

def pick_randomWeight_from_list(food_id_Series,weightSeries):
    "from food_id_list pick food_id with weight"
    weightSeries = pd.Series(weightSeries)
    weightSeries = weightSeries / weightSeries.sum()
    food_id = np.random.choice(food_id_Series,1,p=weightSeries)
    return food_id


def yes_or_no_loop(data,weights):
    result = []
    #print("\n음식을 추천해드립니다!\n")
    count = 0 
    while(count < 300):
        count+=1
        food_id = pick_randomWeight_from_list(list(weights["food_id"]),list(weights["weight"]))
        index = list(data["food_id"].values).index(food_id)
        randomFood = data["food"][index]
        #print(pickedCategory,"-",randomFood)
        result.append([index+1,randomFood])
    return result


def pick_main():
    food_data = pd.read_excel(FOOD_DATA)
    weights = calWeightFromLog(1)[0]
    weights["weight"] = pd.Series([0.066666]*5+[0.0266666]*25)
    weights["weight"] = weights["weight"] / weights["weight"].sum()
    print(weights)
    result = yes_or_no_loop(food_data,weights)
    return result,weights


w,w2  = pick_main()
w2 = w2.sort_index()
w3 = []
for i in w:
    w3.append(i[0])
    
w3 = pd.Series(w3)
w4 = w3.value_counts()
w4 = w4.sort_index()


w5 = calWeightFromLog(1)
w6 = w5[0]
w6 = w6.sort_index()
w7 = w2.weight - w6.weight
w7 =w7.apply(abs)
print(w7.sum() / len(w7))
