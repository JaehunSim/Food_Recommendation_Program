# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
from pathlib import Path
home = str(Path.home())
PATH = home + "\\Desktop\\ee_grad_project\\"

IDDB = PATH + "dataFile\\id_db_log.xlsx"
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def load_id_db():
    id_data = pd.read_excel(IDDB, dtype=np.dtype(str))
    return id_data

def make_new_account():
    data = load_id_db()
    create = "fail"
    
    IDVerify = False
    while True:
        #회원가입 ID, password 반복문
        newID = input("<회원가입을 종료하려면 exit을 입력>\n만드실 Email-ID를 입력하세요.\nEmail-ID: ")
        while True:
            #ID 조건 반복문
            if newID == "exit":
                return
            if not EMAIL_REGEX.match(newID):
                print("<올바른 형식의 Email-ID를 입력하세요.>")
            elif newID in data.id.values:
                print("<이미 존재하는 Email-ID입니다.>")
            else:
                IDVerify = True
            if IDVerify == True:
                break
            newID = input("만드실 Email-ID를 다시 입력하세요.\nEmail-ID: ")
        
        password = input("<시작으로 돌아가려면 start를 입력, 회원가입을 종료하려면 exit을 입력>\n비밀번호를 입력하세요.\nEmail-ID: %s\nPassword: " %(newID))
        while True:
            #password 반복문
            if password == "exit":
                return
            if password == "start":
                break
            password2 = input("비밀번호를 다시 입력해주세요(확인용)\nPassword: ")
            #make new account complete
            if password == password2:
                create = "success"
                break
            password = input("<비밀번호가 서로 다릅니다.>\n비밀번호를 다시 입력하세요.\nID: %s\nPassword: " %(newID))
        
        if create == "success":
            break
    #제공된 ID, password를 DB에 넣기
    ## age, sex 입력받기
    ageVerify = False
    age = input("<회원가입이 거의 다 마쳤습니다.>\n<이 항목들은 빈칸이나 p를 입력시 지나칠 수 있습니다.>\n나이와 성별을 입력해주세요.\n나이: ")
    while True:
        #age 입력 반복문
        if age in ["", " ","  ","   ","p","P"]:
            age = np.nan
            break
        try:
            #age 조건 성립
            if(int(age) in range(1,100)):
                ageVerify = True              
        except:
            pass
        if ageVerify == True:
            break
        age = input("올바르지 못한 입력값입니다. 다시 입력해주세요.\n나이: ")
    
    sexVerify = False
    sex = input("<남성:1, 여성:2>\n성: ")
    while True:
        #sex 입력 반복문
        if sex in ["", " ","  ","   ","p","P"]:
            sex = np.nan
            break
        try:
            #sex 조건 성립
            if int(sex) in [1,2]:
                sexVerify = True              
        except:
            pass
        if sexVerify == True:
            break
        sex = input("올바르지 못한 입력값입니다. 다시 입력해주세요.\n성: ")
    print("<회원가입 성공!>")
    data = data.append({"id_code":str(len(data)+1),"id":newID,"password":password, "age":age, "sex":sex},ignore_index=True)
    data.to_excel(IDDB, index=None)
    #return data
        
def login(data):
    #Input: IDDB
    login = "fail"
    while True:
        #ID/Password 입력 반복문
        ID = input("<회원가입을 하려면 new를 입력, 종료하려면 exit을 입력>.\nEmail-ID를 입력하세요.\nEmail-ID: ")
        if ID == "new":
            make_new_account()
            data = load_id_db()
            ID = input("<회원가입을 하려면 new를 입력, 종료하려면 exit을 입력>.\nEmail-ID를 입력하세요.\nEmail-ID: ")
        if ID == "exit":
            return False
        if ID not in data.id.values:
            while True:
                #ID 입력 반복문
                ID = input("등록되지 않은 Email-ID입니다.\nEmail-ID를 다시 입력하세요.\nEmail-ID: ")
                if ID in data.id.values:
                    break
                if ID  == "exit":
                    return False
                if ID == "new":
                    make_new_account()
                    data = load_id_db()
                    break
        if ID in data.id.values:
            info = data.loc[data['id']==ID]
            targetPassword = info["password"].values[0]
            password = input("비밀번호를 입력하세요\nPassword: ")
            if password == "exit":
                return False
            ##login complete
            if password == targetPassword:
                login = "success"
            while password != targetPassword:
                #password 입력 반복문
                print("Wrong Password")
                print("<시작으로 돌아가려면 start를 입력, 종료하려면 exit을 입력>")
                password = input("비밀번호를 다시 입력하세요\nPassword: ")
                if password in ["start","exit"]:
                    break
                if password == targetPassword:
                    login = "success"
                    break      
            if password == "exit":
                return False
        #login complete
        if login =="success":
            print("\n로그인 성공!\n")
            return  info["id_code"].values[0]

"""
def main():
    data = load_id_db()
    id_code = login(data)
    
        
                
                
w = load_id_db()
w2 = login(w)
#main()
"""
