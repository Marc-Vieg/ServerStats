import os
import sqlite3
import time


class BotData:
    def __init__(self):
        self.data = {
            'timing': [],
            'cpu': [],
            'mem': [],
            'temp': []
        }

        self.db = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))
                                  + "/data", check_same_thread=False)
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS \
                        stats(timing INTEGER PRIMARY KEY, \
                        cpu INTEGER, mem INTEGER, temp INTEGER)''')
            self.db.commit()
        except sqlite3.OperationalError:
            print("database already exist")
        self.charges()
        self.show()

    def charges(self):
        self.cursor.execute('''SELECT timing, cpu, mem, temp FROM stats''')
        all_rows = self.cursor.fetchall()
        for row in all_rows:
            self.data['timing'].append(row[0])
            self.data['cpu'].append(row[1])
            self.data['mem'].append(row[2])
            self.data['temp'].append(row[3])

    def populate(self):
        i = 0
        for t in self.data['timing']:
            try:
                print(("adding ", self.data['timing'][i]))
                self.cursor.execute('''INSERT INTO stats(timing, cpu, mem, temp)
                                     VALUES(?,?,?,?)''',
                                    (int(self.data['timing'][i]),
                                     int(self.data['cpu'][i]),
                                     int(self.data['mem'][i]),
                                     int(self.data['temp'][i])))
                self.db.commit()
                i += 1
            except sqlite3.IntegrityError:
                print(('Record already exists : ', self.data['timing']))

    def show(self):
        dataSize = len(self.data['timing'])
        for idx in range(dataSize):
            print(f"timing : {self.data['timing'][idx]} - ",
                  f"cpu : {self.data['cpu'][idx]} - ",
                  f"mem : {self.data['mem'][idx]} - ",
                  f"temp : {self.data['temp'][idx]}°C")

    def appendData(self, cpu, mem, temp):
        t = round(time.time())
        self.data['timing'].append(t)
        self.data['cpu'].append(round(cpu))
        self.data['mem'].append(round(mem))
        self.data['temp'].append(round(temp))
        try:
            self.cursor.execute('''INSERT INTO stats(timing, cpu, mem, temp)
                                VALUES(?,?,?,?)''', (t, cpu, mem, temp))
            self.db.commit()
        except sqlite3.IntegrityError:
            print('Record already exists')

    def getfromData(self, date):
        self.cursor.execute('''SELECT timing, cpu, mem, \
                            temp FROM stats WHERE timing=?''', (date,))
        data = self.cursor.fetchone()
        return data[1], data[2], data[3]

    def getFirstData(self):
        self.cursor.execute('''SELECT timing FROM stats''')
        data = self.cursor.fetchone()
        return data[0]

    def flushData(self):
        self.cursor.execute('''DROP stats''')
        self.data = {
            'timing': [],
            'cpu': [],
            'mem': [],
            'temp': []
        }
        return "Data are deleted !"
