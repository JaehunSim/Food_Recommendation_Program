# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import random

data = pd.read_excel("C://Users//tapu1//Desktop//ee_grad_project//survey//images//imageList.xlsx")

sample = data.name.sample(120, replace=True)
