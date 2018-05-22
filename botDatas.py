import sqlite3
import time
import json




Datas = dict()
Datas['timing'] = []
Datas['cpu'] = []
Datas['mem'] = []
Datas['temp'] = []

db = sqlite3.connect('datas', check_same_thread=False)
try :
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE stats(timing INTEGER PRIMARY KEY, cpu INTEGER, mem INTEGER, temp INTEGER)''')
    db.commit()
except sqlite3.OperationalError:
    print("database already exist")

def charges():
    global Datas
    cursor = db.cursor()
    cursor.execute('''SELECT timing, cpu, mem, temp FROM stats''')
    all_rows = cursor.fetchall()
    for row in all_rows:
        print('timing {0} : cpu {1}, mem {2}, temp {3}'.format(row[0], row[1], row[2], row[3]))
        Datas['timing'].append(row[0])
        Datas['cpu'].append(row[1])
        Datas['mem'].append(row[2])
        Datas['temp'].append(row[3])


def populate():
    global Datas
    i = 0
    for t in Datas['timing']:
        try:
            print(("adding ", Datas['timing'][i]))
            with db:
                cursor = db.cursor()
                cursor.execute('''INSERT INTO stats(timing, cpu, mem, temp)
                      VALUES(?,?,?,?)''', (int(Datas['timing'][i]), int(Datas['cpu'][i]), int(Datas['mem'][i]), int(Datas['temp'][i])))
                db.commit()
                i+=1
        except sqlite3.IntegrityError:
            print(('Record already exists : ', Datas['timing']))

def show():
    cursor = db.cursor()
    cursor.execute('''SELECT timing, cpu, mem, temp FROM stats''')
    all_rows = cursor.fetchall()
    tDatas = dict()
    tDatas['timing'] = []
    tDatas['cpu'] = []
    tDatas['mem'] = []
    tDatas['temp'] = []
    for row in all_rows:
        print("timing : ", row[0], " - ", row[1], " - ", row[2], " - ", row[3], "C")
        tDatas['timing'].append(row[0])
        tDatas['cpu'].append(row[1])
        tDatas['mem'].append(row[2])
        tDatas['temp'].append(row[3])
    print(str(tDatas))


def appendData(cpu, mem, temp):
    t = round(time.time())
    Datas['timing'].append(t)
    Datas['cpu'].append(round(cpu))
    Datas['mem'].append(round(mem))
    Datas['temp'].append(round(temp))
    try:
        with db:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO stats(timing, cpu, mem, temp)
                  VALUES(?,?,?,?)''', (t, cpu, mem, temp))
            db.commit()
    except sqlite3.IntegrityError:
        print('Record already exists')


def getfromDatas(date):
    cursor = db.cursor()
    cursor.execute('''SELECT timing, cpu, mem, temp FROM stats WHERE timing=?''', (date,))
    data = cursor.fetchone()
    return data[1], data[2], data[3]

def getFirstData():
    cursor = db.cursor()
    cursor.execute('''SELECT timing FROM stats''')
    data = cursor.fetchone()
    return data[0]



if __name__ == '__main__':
    charges()
    #populate()
    show()


