# coding: utf-8

# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib
import warnings

warnings.filterwarnings("ignore")

#한글 폰트 출력
font_name = matplotlib.font_manager.FontProperties(fname='C:\\Windows\\Fonts\\malgun.ttf').get_name()

#pd.set_option('display.height', 1000)
#pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 1000)




home = str(Path.home())
PATH = home + "\\Desktop\\ee_grad_project\\"
STRENGTH = 2



#def printDF(df):
 #   return df.style.set_table_styles([{'selector': '', 'props': [('border', '4px solid #7a7')]}])


def getFoodData():
    data = pd.read_excel(PATH+"dataFile\\food_data.xlsx")
    
    temp = []
    foodCategoryList = list(data["category"].unique())
    
    foodTypeList = []
    for i in range(len(data)):
        food = data.iloc[i,:]
        temp2 = []
        #temp2.append(food["category"])
        for j in food["type"].split(" "):
            temp2.append(j)
            if j not in foodTypeList:
                foodTypeList.append(j)
        temp.append(temp2)
    
    data["typeCombine"] = temp

    return foodCategoryList, foodTypeList, data


def getBaseWeight():
    foodCategoryList, foodTypeList, data = getFoodData()
    for type1 in foodTypeList:
        temp =[]
        for index in data["typeCombine"].index:
            if type1 in data["typeCombine"][index]:
                temp.append(index)
        data[type1] = False
        for index in temp:
            data[type1][index]= True
    
    #base Category Weight
    temp = data["category"]
    bcws = pd.Series(temp.value_counts() / temp.count(), index=foodCategoryList)
    typeData = data.iloc[:,[5,6,7,8,9,10,11,12,13,14,15,16]][data==True].values
    
    
    for i in range(len(typeData)):
        temp = typeData[i]
        typeData[i] = (temp / np.count_nonzero(temp==True))
    
    data.iloc[:,[5,6,7,8,9,10,11,12,13,14,15,16]] = typeData
    
    #baseTypeWeight
    dataTypeCount = data.iloc[:,[5,6,7,8,9,10,11,12,13,14,15,16]].sum()
    btws = pd.Series(dataTypeCount / dataTypeCount.sum(),index = foodTypeList)
    
    data["weight"] = 1 / len(data["food_id"])
    baseWeight = data.iloc[:,[0,len(data.columns)-1]]
    
    return foodCategoryList, foodTypeList, data, bcws, btws,baseWeight

foodCategoryList, foodTypeList, data, bcws, btws, baseWeight = getBaseWeight()

def calWeightFromLog(id_code,foodCategoryList=foodCategoryList, foodTypeList=foodTypeList,data=data,bcws=bcws,btws=btws):
    logData = pd.read_excel(PATH + "dataFile\\output_log.xlsx")
    needData = logData[logData["id_code"] == id_code].iloc[:,[1,2]]
    #return needData
    #print("22222222")
    if len(needData)==0:
        return baseWeight, data
    basePath = PATH + "dataFile\\weighted.xlsx"    
    weight = pd.read_excel(basePath)
    w = needData.groupby("food_id").count()
    #print("33333")
    w2 = pd.Series(0,index=range(1,31))
    for i in w.index:
        w2[i] = w.loc[i]
    
    profile = []
    for column in weight.columns[2:]:
        profile.append((weight[column] * w2).sum())
    preference = (weight.iloc[:,2:] * profile).sum(axis=1)
    preference = preference / preference.sum()
    preference.name = "weight"
    preference = pd.DataFrame(preference)
    preference["food_id"] = range(1,31)
    preference = preference.iloc[:,[1,0]]
    return preference, data

