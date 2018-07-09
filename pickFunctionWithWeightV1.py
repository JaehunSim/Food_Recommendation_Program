# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
from pathlib import Path
home = str(Path.home())
PATH = home + "\\Desktop\\ee_grad_project\\"

import os
os.chdir(PATH)

#my library
from foodDataWeightFromLogV3 import calWeightFromLog
from foodDataWeightFromLogV2 import calWeightFromLog as calWeightFromLogProto

OUTPUT = PATH +  "dataFile\\output_log.xlsx"
FOOD_DATA = PATH + "dataFile\\food_data.xlsx"

def pick_randomWeight_from_list(food_id_Series,weightSeries):
    "from food_id_list pick food_id with weight"
    food_id = np.random.choice(food_id_Series,1,p=weightSeries)
    return food_id


def yes_or_no_loop(data,id_code,weights):
    noChoiceList = []
    choice = 0
    print("\n음식을 추천해드립니다!\n")
    while(choice == 0):

        if len(noChoiceList) == list(data["food_id"])[-1]:
            print("더 이상 추천해줄 음식이 없습니다.")
            choice = "EXIT"
            break
        
        food_id = pick_randomWeight_from_list(list(weights["food_id"]),list(weights["weight"]))
        index = list(data["food_id"].values).index(food_id)
        randomFood, pickedCategory = data["food"][index], data["category"][index]
        #음식리스트 전부가 마음에 안들경우 출력
        
        #골랐던 음식이 마음에 안든 경우 이를 제외 추천
        if randomFood in noChoiceList:
            continue
        
        print(pickedCategory,"-",randomFood)
        while(True):
            choice = input("Yes or No? ")
            choice = choice.upper()
            if choice in ["Y","YES","EXIT"]:
                break
            elif choice in ["N", "NO"]:
                print()
                choice = 0
                noChoiceList.append(randomFood)
                break
            else:
                print("Wrong Input")
    if choice == "EXIT":
        randomFood = "Dump"
    return randomFood, noChoiceList

def pick_main(id_code):
    food_data = pd.read_excel(FOOD_DATA)
    try:
        log_data= pd.read_excel(OUTPUT)    
    except:
        log_data = pd.DataFrame(columns=["id_code","food_id","choice","time","gps","weather","temp"])
    #print("1111111")
    logData = pd.read_excel(PATH + "dataFile\\output_log.xlsx")
    needData = logData[logData["id_code"] == id_code]
    
    if len(needData) >= 20:   
        weights = calWeightFromLog(id_code)[0]
    else:
        weights = calWeightFromLogProto(id_code)[0]
    weights["weight"] = weights["weight"] / weights["weight"].sum()
    print(weights)
    randomFood, noChoiceList = yes_or_no_loop(food_data, id_code,weights)
    for food in noChoiceList:
        food_id = food_data.loc[food_data["food"]==food]["food_id"].values[0]
        log_data = log_data.append({"id_code":id_code, "food_id":food_id, "choice":0, "time":datetime.datetime.now(), "gps":np.nan, "weather":np.nan, "temp":np.nan},ignore_index=True)
    if randomFood == "Dump":
        pass
    else:
        food_id = food_data.loc[food_data["food"]==randomFood]["food_id"].values[0]
        log_data = log_data.append({"id_code":id_code, "food_id":food_id, "choice":1, "time":datetime.datetime.now(), "gps":np.nan, "weather":np.nan, "temp":np.nan},ignore_index=True)
    #return log_data
    log_data.to_excel(OUTPUT, index=None)
    #return log_data
    
#w  = pick_main(1)
