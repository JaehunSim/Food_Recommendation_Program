# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
from tabulate import tabulate #print DataFrame neat
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib

#한
font_name = matplotlib.font_manager.FontProperties(fname='C:\\Windows\\Fonts\\malgun.ttf').get_name()

home = str(Path.home())
PATH = home + "\\Desktop\\ee\\"

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

#def calWeightFromLog(id_code):

id_code = 5


foodCategoryList, foodTypeList, data = getFoodData()

for type1 in foodTypeList:
    temp =[]
    for index in data["typeCombine"].index:
        if type1 in data["typeCombine"][index]:
            temp.append(index)
    data[type1] = False
    for index in temp:
        data[type1][index]= True

data = data.drop(["type","typeCombine"],axis=1)
data.style.set_table_styles([{'selector': '', 'props': [('border', '4px solid #7a7')]}])

"""
logData = pd.read_excel(PATH + "dataFile\\output_log.xlsx")
needData = logData[logData["id_code"] == id_code]

rejected = needData[needData["choice"]==0]
rejectedIDList = list(rejected["food_id"])
rejectedCategoryList = []
rejectedTypeList = []
for food_id in rejectedIDList:
    tempData = data[data["food_id"]==food_id]
    rejectedCategoryList.append(tempData["category"].values[0])
    for type1 in tempData["typeCombine"].values[0]:
        rejectedTypeList.append(type1)
    #print(tabulate(data[data["food_id"]==food_id], headers="keys", tablefmt="psql"))
    
approved = needData[needData["choice"]==1]
approvedIDList = list(approved["food_id"])
approvedCategoryList = []
approvedTypeList = []
for food_id in approvedIDList:
    tempData = data[data["food_id"]==food_id]
    approvedCategoryList.append(tempData["category"].values[0])
    for type1 in tempData["typeCombine"].values[0]:
        approvedTypeList.append(type1)

#base Category Weight
temp = data["category"]
bcws = pd.Series(temp.value_counts() / temp.count(), index=foodCategoryList)

#baseTypeWeight
btw = [1* (1/len(foodTypeList))] *len(foodTypeList)
btws = pd.Series(btw, index=foodTypeList, name="Weight")

#ApprovedCategorySeries
acs = pd.Series(0,index=foodCategoryList)
for i in approvedCategoryList:
    acs[i] += 1  
    
#approvedTypeSeries
ats = pd.Series(0,index=foodTypeList)
for i in approvedTypeList:
    ats[i] += 1      

#rejecctedCategorySeries
rcs = pd.Series(0,index=foodCategoryList)
for i in rejectedCategoryList:
    rcs[i] += 1

#rejecctedTypeSeries
rts = pd.Series(0,index=foodTypeList)
for i in rejectedTypeList:
    rts[i] += 1     

#standard normal distribution
mu = 0
std = 1
rv = scipy.stats.norm(mu, std)


#acs
##normalization
acs_norm = (acs - acs.mean()) / (acs.max() - acs.min())
converted = rv.cdf(acs_norm)
##converted Sum into One
cso = converted / converted.sum()
bcws2 = bcws +  (cso - bcws) / 1.5

#ats
##normalization
ats_norm = (ats - ats.mean()) / (ats.max() - ats.min())
converted = rv.cdf(ats_norm)
##converted Sum into One
cso2 = converted / converted.sum()
btws2 = btws + (cso2 - btws) / 1.5



#rcs
##normalization
rcs_norm = (rcs - rcs.mean()) / (rcs.max() - rcs.min())
converted = rv.cdf(rcs_norm.values)
##converted Sum into One
cso = converted / converted.sum()
cso = cso
bcws2 += (bcws2 -cso) / 1.5

#rts
##normalization
rts_norm = (rts - rts.mean()) / (rts.max() - rts.min())
converted = rv.cdf(rts_norm)
##converted Sum into One
cso2 = converted / converted.sum()
btws2 += (cso2 - btws2) / 1.5

"""