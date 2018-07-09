# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
home = str(Path.home())
PATH = home + "\\Desktop\\ee_grad_project\\"

basePath = PATH + "dataFile\\base.xlsx"

base = pd.read_excel(basePath)

DF = base.count()[2:]
IDF = DF.sum()/ DF
IDF = np.log10(IDF)

base["sum"] = base.count(axis=1)-2

for column in base.columns[2:-1]:
    base[column] = base[column]/ base["sum"]**0.5
    
base = base.iloc[:,:-1]

for index in base.index:
    base.iloc[index,2:] = base.iloc[index,2:] * IDF
    
base.to_excel(PATH+"dataFile\\weighted.xlsx",index=None,encoding="euc-kr")
