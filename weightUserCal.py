# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
home = str(Path.home())
PATH = home + "\\Desktop\\ee_grad_project\\"

basePath = PATH + "dataFile\\weighted2.xlsx"
responsePATH = PATH + "dataFile\\food_selection_responses2.xlsx"

weight = pd.read_excel(basePath)
response = pd.read_excel(responsePATH)

responseList = []
for index in response.index:
    temp = response.iloc[index,4:]
    temp = temp.sort_index()
    temp.index = range(0,30)
    responseList.append(temp)

preferenceList = []

for response1 in responseList:
    w = response1   
    profile = []
    for column in weight.columns[2:]:
        profile.append((weight[column] * w).sum())
    
    preference = (weight.iloc[:,2:] * profile).sum(axis=1)
    preference = preference / preference.sum()
    preferenceList.append(preference)

compareList = []
pointList = []
for i in range(len(responseList)):
    tempData = weight.iloc[:,[0,1]].copy()
    tempData["response"] = responseList[i]
    tempData["preference"] = preferenceList[i]
    positiveCount = tempData["response"][tempData["response"]==1].count()
    positRate = positiveCount / tempData["response"].count() 
    calData = tempData.sort_values("preference",ascending=False)[:positiveCount]
    evaluateRate = calData["response"][calData["response"]==1].count() / positiveCount
    finalPoint = round(evaluateRate - positRate,5)
    compareList.append(positRate)
    pointList.append(finalPoint)

compareList = np.array(compareList)
pointList = np.array(pointList)
algList = compareList + pointList
pointList = pd.Series(pointList[pointList!=0])
#pointListSamp = pointList.sample(frac=0.7)
print(round(pointList.mean(),4) * 100,"%",sep="")

compareList = compareList[compareList!=1]
algList = algList[algList != 1]

print(round(compareList.mean(),4) * 100,"%",sep="")
print(round(algList.mean(),4) * 100,"%",sep="")
