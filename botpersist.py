# -*- coding: utf-8 -*-
import json
from botglobalvars import MyGlobals

def save():
    with open('botDatas.json', 'w') as f:
        try:
            json.dump(MyGlobals.Datas, f)
        except:
            print("erreur d ecriture de la db")

def Charges():
    global Datas
    try:
        with open('botDatas.json') as f:
            MyGlobals.Datas = json.load(f)
            print("on charges le dataset")
            return 1
    except:
        print("erreur d'ouverture de la db'")
        return "err_openfile"











