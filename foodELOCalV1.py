# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pathlib import Path
import scipy.stats
import matplotlib
import warnings
warnings.filterwarnings("ignore")

#한글 폰트 출력
font_name = matplotlib.font_manager.FontProperties(fname='C:\\Windows\\Fonts\\malgun.ttf').get_name()

home = str(Path.home())
PATH = home + "\\Desktop\\ee_grad_project\\"
STRENGTH = 2


MEAN_ELO = 1500
ELO_WIDTH = 400
K_FACTOR = 64

def getFoodData():
    data = pd.read_excel(PATH+"dataFile\\food_data.xlsx")
    
    temp = []
    foodCategoryList = list(data["category"].unique())
    foodCategoryList.sort()
    
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

    return pd.Series(foodCategoryList), pd.Series(foodTypeList), data

def expected_result(elo_a, elo_b):
    """
    https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
    """
    expect_a = 1.0/(1+10**((elo_b - elo_a)/ELO_WIDTH))
    return expect_a


def update_elo(winner_elo, loser_elo, num=1, neg=False):
    """
    https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
    """
    if neg==False:
        neg = 1
    else:
        neg = -1
    expected_win = expected_result(winner_elo, loser_elo)
    change_in_elo = K_FACTOR * (1-expected_win) / num * neg
    winner_elo += change_in_elo
    loser_elo -= change_in_elo
    return winner_elo, loser_elo


foodCategoryList, foodTypeList, data = getFoodData()

logData = pd.read_excel(PATH + "dataFile\\output_log.xlsx")

id_code = 5
needData = logData[logData["id_code"] == id_code]
needData = needData.join(data.iloc[:,[0,1]].set_index('food_id'), on='food_id')
needData.index= range(len(needData))

n_teams = len(foodCategoryList)
current_elos = np.ones(shape=(n_teams)) * MEAN_ELO
choiceNum = len(needData)

df_food_elos = pd.DataFrame(index= range(choiceNum),columns=range(n_teams))
approve = needData[needData["choice"] == 1].iloc[:,[1,7]]
reject = needData[needData["choice"] == 0].iloc[:,[1,7]]

foodList = pd.DataFrame(data["food_id"])
foodListCate = foodList.join(data.iloc[:,[0,1]].set_index('food_id'), on='food_id')

for row in approve.itertuples():
    idx = row.Index
    w_id = row.category
    l_list = foodCategoryList.drop(foodCategoryList[foodCategoryList==w_id].index[0])
    
    for l_id in l_list:
        w_elo_before = current_elos[foodCategoryList[foodCategoryList==w_id].index[0]]
        l_elo_before = current_elos[foodCategoryList[foodCategoryList==l_id].index[0]]
        w_elo_after, l_elo_after = update_elo(w_elo_before, l_elo_before, len(foodCategoryList))
        
    current_elos[foodCategoryList[foodCategoryList==w_id].index[0]] = w_elo_after
    current_elos[foodCategoryList[foodCategoryList==l_id].index[0]] = l_elo_after
    
for row in reject.itertuples():
    idx = row.Index
    w_id = row.category
    l_list = foodCategoryList.drop(foodCategoryList[foodCategoryList==w_id].index[0])
    
    for l_id in l_list:
        w_elo_before = current_elos[foodCategoryList[foodCategoryList==w_id].index[0]]
        l_elo_before = current_elos[foodCategoryList[foodCategoryList==l_id].index[0]]
        w_elo_after, l_elo_after = update_elo(w_elo_before, l_elo_before, len(foodCategoryList),neg=True)
        
    current_elos[foodCategoryList[foodCategoryList==w_id].index[0]] = w_elo_after
    current_elos[foodCategoryList[foodCategoryList==l_id].index[0]] = l_elo_after
    
mu = 0
std = 1
rv = scipy.stats.norm(mu, std)

current_elos_norm = (current_elos - current_elos.mean()) / (current_elos.max() - current_elos.min())
converted = rv.cdf(current_elos_norm)
converted = pd.Series(converted / converted.sum())
converted.index = foodCategoryList.values
resultList = []
for j in range(300):
    n_samples = 20
    samples = approve.sample(n_samples)
    approveCount = samples.category.value_counts()
    approveCount = approveCount.sort_index()
    approveCount = approveCount / approveCount.sum()
    result1 = ((converted - approveCount) **2).sum()
    resultList.append(result1)
resultList = pd.np.array(resultList)
print(K_FACTOR, resultList.mean())