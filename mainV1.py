# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
home = str(Path.home())
PATH = home + "\\Desktop\\ee_grad_project\\"

#my library
from pickFunctionWithWeightV1 import pick_main
from makeNewAccountAndLoginV1 import load_id_db, login

OUTPUT = PATH + "dataFile\\output_log.xlsx"

def clearLog():
    log_data = pd.DataFrame(columns=["id_code","food_id","choice","time","gps","weather","temp"])
    log_data.to_excel(OUTPUT, index=None)

def main():
    #ID_data load
    ID_data = load_id_db()
    #login
    id_code = login(ID_data)
    if id_code == False:
        print("\n종료")
        return
    
    #pick food and save log
    for i in range(15):
        pick_main(int(id_code))

    print("식사 맛있게 하세요!")

#clearLog()

main()