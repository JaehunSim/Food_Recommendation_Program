# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
from pathlib import Path
home = str(Path.home())
PATH = home + "\\Desktop\\ee\\"

RECOMMEND_LIST = PATH + "dataFile\\food_recommendV2.xlsx"
OUTPUT = PATH +  "dataFile\\output_log.xlsx"
FOOD_DATA = PATH + "dataFile\\food_data.xlsx"

def pick_random_from_list(list1):
    "from list1 pick random value"
    randIndex = np.random.randint(0,len(list1))
    return list1[randIndex]

def yes_or_no_loop(data):
    "append column names from data"
    data_category_list=[]
    for name in data:
        data_category_list.append(name)
    noChoiceList = []
    choice = 0
    print("\n음식을 추천해드립니다!\n")
    
    while(choice == 0):
        pickedCategory = pick_random_from_list(data_category_list)
        categoryData = data[pickedCategory]
        categoryData = categoryData.dropna()
        randomFood = list(categoryData.sample(1))[0]
        
        #음식리스트 전부가 마음에 안들경우 출력
        if len(noChoiceList) == data.count().sum():
            print("더 이상 추천해줄 음식이 없습니다.")
            choice = "EXIT"
            break
        
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
    recommend_data = pd.read_excel(RECOMMEND_LIST)
    food_data = pd.read_excel(FOOD_DATA)
    try:
        log_data= pd.read_excel(OUTPUT)    
    except:
        log_data = pd.DataFrame(columns=["id_code","food_id","choice","time","gps","weather","temp"])
    randomFood, noChoiceList = yes_or_no_loop(recommend_data)
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
#pick_main(1)
