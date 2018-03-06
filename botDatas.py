import json
import time

Datas = dict()
Datas['timing'] = []
Datas['cpu'] = []
Datas['mem'] = []
Datas['temp'] = []


def appendData(cpu, mem, temp):
    Datas['timing'].append(round(time.time()))
    Datas['cpu'].append(round(cpu))
    Datas['mem'].append(round(mem))
    Datas['temp'].append(round(temp))


def save():
    with open('Datas.json', 'w') as f:
        try:
            json.dump(Datas, f)
        except:
            print("erreur d ecriture de la db")


def charges():
    global Datas
    try:
        with open('Datas.json') as f:
            Datas = json.load(f)
            print("on charges le dataset")
            return 1
    except:
        print("erreur d'ouverture de la db'")
        return "err_openfile"


def getfromDatas(date):
    return  Datas['cpu'][Datas['timing'].index(date)], \
             Datas['mem'][Datas['timing'].index(date)], \
              Datas['temp'][Datas['timing'].index(date)]

