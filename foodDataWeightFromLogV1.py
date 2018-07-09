# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
from tabulate import tabulate #print DataFrame neat
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib
import warnings

warnings.filterwarnings("ignore")

#한글 폰트 출력
font_name = matplotlib.font_manager.FontProperties(fname='C:\\Windows\\Fonts\\malgun.ttf').get_name()

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

home = str(Path.home())
PATH = home + "\\Desktop\\ee\\"
strength = 2

def printDF(df):
    return df.style.set_table_styles([{'selector': '', 'props': [('border', '4px solid #7a7')]}])

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

#standard normal distribution
mu = 0
std = 1
rv = scipy.stats.norm(mu, std)


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

#baseTypeWeight
btw = [1* (1/len(foodTypeList))] *len(foodTypeList)
btws = pd.Series(btw, index=foodTypeList, name="Weight")

#def calWeightFromLog(id_code):

id_code = 5

logData = pd.read_excel(PATH + "dataFile\\output_log.xlsx")
needData = logData[logData["id_code"] == id_code]


approved = needData[needData["choice"]==1]
approvedIDList = list(approved["food_id"])
approvedCategoryList = []
approvedTypeList = []
for food_id in approvedIDList:
    tempData = data[data["food_id"]==food_id]
    approvedCategoryList.append(tempData["category"].values[0])
    for type1 in tempData["typeCombine"].values[0]:
        approvedTypeList.append(type1)

#ApprovedCategorySeries
acs = pd.Series(0,index=foodCategoryList)
for i in approvedCategoryList:
    acs[i] += 1

#approvedTypeSeries
ats = pd.Series(0,index=foodTypeList)
for i in approvedTypeList:
    ats[i] += 1

rejected = needData[needData["choice"]==0]
rejectedIDList = list(rejected["food_id"])
rejectedCategoryList = []
rejectedTypeList = []
for food_id in rejectedIDList:
    tempData = data[data["food_id"]==food_id]
    rejectedCategoryList.append(tempData["category"].values[0])
    for type1 in tempData["typeCombine"].values[0]:
        rejectedTypeList.append(type1)

#rejecctedCategorySeries
rcs = pd.Series(0,index=foodCategoryList)
for i in rejectedCategoryList:
    rcs[i] += 1

#rejecctedTypeSeries
rts = pd.Series(0,index=foodTypeList)
for i in rejectedTypeList:
    rts[i] += 1

#acs
##normalization
acs_norm = (acs - acs.mean()) / (acs.max() - acs.min())
converted = rv.cdf(acs_norm)
##converted Sum into One
cso = converted / converted.sum()
bcws2 = bcws +  (cso - bcws) / strength

#ats
##normalization
ats_norm = (ats - ats.mean()) / (ats.max() - ats.min())
converted = rv.cdf(ats_norm)
##converted Sum into One
cso2 = converted / converted.sum()
btws2 = btws + (cso2 - btws) / strength

#rcs
##normalization
if rcs.max() != 0:
    rcs_norm = (rcs - rcs.mean()) / (rcs.max() - rcs.min())
    converted = rv.cdf(rcs_norm.values)
    ##converted Sum into One
    cso = converted / converted.sum()
    bcws2 += (bcws2 -cso) / strength

#rts
##normalization
if rts.max() != 0:
    rts_norm = (rts - rts.mean()) / (rts.max() - rts.min())
    converted = rv.cdf(rts_norm)
    ##converted Sum into One
    cso2 = converted / converted.sum()
    btws2 += (cso2 - btws2) / strength

print(bcws)
print(bcws2)

print(btws)
print(btws2)

tempList = []
for i in range(len(data)):
    temp = 0
    temp +=bcws2[data["category"][i]]
    for type1 in data["typeCombine"][i]:
        temp += (btws2[type1]/len(data["typeCombine"][i]))
    tempList.append(temp)
tempList = np.array(tempList)
tempList = tempList / tempList.sum()
data["weight"] = tempList

printDF(data.iloc[:,[0,2,-1]])

