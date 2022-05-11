# -*- coding: utf-8 -*-

from datetime import datetime, date
import ipaddress
import matplotlib
import matplotlib.pyplot as plt
import operator
import os
import psutil
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement
import re
import speedtest
import shlex
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time
import urllib
matplotlib.use("Agg")


class BotTools:
    """
    This is a tools box object, which defines all method
    used by the bot.

    All method should return :

    - A boolean for the method status :
        * True if all is okay
        * False if error raised

    - A string or a tuple, for the result of the method:
        * tuple contains mainly a picture result on first item,
        and a boolean to indicate this is a send Picture instead of a
        send Message
    """
    def __init__(self, botConfig, botData):
        # self.bot = telepot.Bot(botConfig.TOKEN)
        self.botConfig = botConfig
        self.botData = botData
        self.sendPicture = True

# ############ Tools #############

    def _plotbiggraph(self, Datas, xaxis, tmperiod):
        """
        Plotting stats for a desired time in the big graph
        with matplotlib.pyplot
        """
        Datas['time'][0] = 0
        xaxis = Datas['time']
        plt.xlabel(tmperiod)
        plt.ylabel('% Used')
        plt.title('Memory, Cpu and Temperature Usage Graph')
        # mem graph
        memorythreshold = self.botConfig.memorythreshold
        plt.text(0.1 * len(xaxis), memorythreshold + 2,
                 'Memory Threshold: ' + str(memorythreshold) + ' %')
        # usage graph
        usagethreshold = self.botConfig.usagethreshold
        plt.text(0.1 * len(xaxis), usagethreshold + 2,
                 'Cpu Threshold: ' + str(usagethreshold) + ' %')
        memthresholdarr, usagethresholdarr = [], []
        for xas in xaxis:
            memthresholdarr.append(memorythreshold)
        for xas in xaxis:
            usagethresholdarr.append(usagethreshold)
        plt.plot(xaxis, memthresholdarr, 'g--',
                 xaxis, usagethresholdarr, 'b--')
        # mem
        Datas['mem'][0] = 0
        plt.plot(xaxis, Datas['mem'], 'g-', label="mem")
        # cpu
        Datas['cpu'][0] = 0
        plt.plot(xaxis, Datas['cpu'], 'b-', label="cpu")
        # temp
        Datas['temp'][0] = 0
        plt.plot(xaxis, Datas['temp'], 'r-.', label="°C")
        j = xaxis[-1]
        plt.axis('auto')

        plt.xlim(0, j)
        plt.ylim(0, 100)

        if os.path.isfile('/tmp/graph.png'):
            os.remove('/tmp/graph.png')

        plt.savefig('/tmp/graph.png')
        plt.close()
        f = open('/tmp/graph.png', 'rb')  # some file on local disk
        return f

    def _recupTemp(self):
        """
        Get temperatures from psutil, and return temperatures[]
        ex : print(temperatures['Core 0']) -> 45
        """
        sensors_raw = psutil.sensors_temperatures()
        sensors_coretemp = str(sensors_raw['coretemp'])
        tmp = []
        testlabel = ''
        temperatures = dict()
        for labelneeded in self.botConfig.myCores:
            while testlabel != labelneeded:
                index = sensors_coretemp.find(labelneeded)
                tempString = sensors_coretemp
                tmp = tempString[index:]
                tmp = tempString.split("'")
                for testlabel in tmp:
                    if testlabel == labelneeded:
                        tmpp = str(tmp)
                        indext = tmpp.find('current=')
                        indext += 8
                        tmpp = tmpp[indext:]
                        temperatures[testlabel] = int(tmpp.split('.')[0])
                        break
        return temperatures

    def _bytes2human(self, n):
        """
        Credits: http://code.activestate.com/recipes/578019
        Thank you fabaff !
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f% s' % (value, s)
        return "%sB" % n

# ############ Utils #############

    def ipCheck(self, myActualIp, lastCheck):
        myIp = None
        if myActualIp == '0':
            myIp = self.getip()
        if round(time.time()) - lastCheck > 600:
            try:
                myIp = self.getip()
            except Exception:
                print("no internet, no ip")
                return 1
            try:
                myIp = ipaddress.ip_address(myIp)
            except Exception:
                print("not a valid ipv4")
                return 1
        return myIp

    def logwatch(self):
        """ Uses the logwatch binary to send one line at a time the summary """
        command = 'logwatch --output stdout --format text |' \
                  + 'while IFS= read -r line;do telegram-send "$line";done'
        p = Popen(command, shell=True, stdin=PIPE, stderr=STDOUT,
                  stdout=PIPE, close_fds=True)
        output = p.stdout.read()
        return output

    def raidstatus(self):
        """ Send the status of possible raid array """
        p = Popen('cat /proc/mdstat | grep md',
                  shell=True, stdin=PIPE, stderr=STDOUT,
                  stdout=PIPE, close_fds=True)
        output = str(p.stdout.read(), 'utf-8')
        return output

    def memgraph(self, value):
        """ preparing stats for the big graph """
        graphDatas = {
            'cpu': [0],
            'mem': [0],
            'temp': [0],
            'time': [0]
        }
        timep = 0
        # get fixed period of stats
        try:
            timeWanted = self.botData.data['timing'][-1] - \
                        self.botConfig.GraphicHours
        except IndexError:
            return "I don't have so much Datas"
        for timing in self.botData.data['timing']:
            if timing in range(timeWanted - 100, timeWanted + 100):
                timep = self.botData.data['timing'].index(timing)
                break
        if timep == 0:
            timep = 10
        i, mem, cpu, temp = 0, 0, 0, 0
        dataTiming = self.botData.data['timing']
        for index in range(len(dataTiming))[timep:len(dataTiming)]:
            cpu, mem, temp = self.botData.getfromData(dataTiming[index])
            graphDatas['cpu'].append(cpu)
            graphDatas['mem'].append(mem)
            graphDatas['temp'].append(temp)
            graphDatas['time'].append(dataTiming[index] - dataTiming[timep])
            i += 1

        if value == 'all':
            try:
                time = graphDatas['time'][-1] - graphDatas['time'][0]
            except IndexError:
                time = -1

            if time < 60:
                xlabel = " last %d secondes" % time
            if 60 <= time < 3600:
                xlabel = " last " + str(round(time / 60)) + " minutes"
            if time >= 3600:
                xlabel = " last " + str(round(time / 3600)) + " hours"
            return True, ((self._plotbiggraph(
                            graphDatas,
                            self.botConfig.xaxis,
                            xlabel
                        ),
                        self.sendPicture
                        ))

    def stats(self):
        """
        Send general stats of the server (cpu usage, memory, disks...)
        """
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            boottime = datetime.fromtimestamp(psutil.boot_time())
            now = datetime.now()
            timedif = "Online for: %.1f Hours" % \
                (((now - boottime).total_seconds()) / 3600)
            memtotal = "Total memory: %.2f GB " % (memory.total / 1000000000)
            memavail = "Available memory: %.2f GB" % \
                (memory.available / 1000000000)
            memuseperc = "Used memory: " + str(memory.percent) + " %"
            diskused = "Disk used: " + str(disk.percent) + " %"
            cpupercent = "Cpu usage: " + str(psutil.cpu_percent(1)) + " %"
            pids = psutil.pids()
            pidsreply, cpusreply = '', ''
            procs, procscpu = {}, {}
            for pid in pids:
                p = psutil.Process(pid)
                try:
                    pmem = p.memory_percent()
                    if pmem > 0.5:
                        if p.name() in procs:
                            procs[p.name()] += pmem
                        else:
                            procs[p.name()] = pmem
                except Exception:
                    print("exception calculating by process memory %")
            sortedprocs = sorted(procs.items(),
                                 key=operator.itemgetter(1), reverse=True)
            for proc in sortedprocs:
                pidsreply += proc[0] + " " + ("%.2f " % proc[1]) + " % mem \n"
            for pid in pids:
                p = psutil.Process(pid)
                try:
                    pcpu = p.cpu_percent(interval=0.01) / psutil.cpu_count()
                    if pcpu > 0.1:
                        if p.name() in procscpu:
                            procscpu[p.name()] += pcpu
                        else:
                            procscpu[p.name()] = pcpu
                except Exception:
                    print("exception calculating by process cpu usage %")
            sortedcpus = sorted(procscpu.items(),
                                key=operator.itemgetter(1),
                                reverse=True)
            for proc in sortedcpus:
                cpusreply += proc[0] + " " + ("%.2f " % proc[1]) + " % cpu \n"
            reply = str(timedif + "\n"
                        + memtotal + "\n"
                        + memavail + "\n"
                        + memuseperc + "\n"
                        + diskused + "\n"
                        + cpupercent + "\n\n"
                        + pidsreply + "\n "
                        + cpusreply + "\n\n")
            return True, reply
        except Exception:
            return False, "Something went wrong on stats"

    def gettemp(self, numeric_result: bool = False):
        """
        Send actual temperatures of the processor from recupTemp()
        """
        try:
            temperatures = self._recupTemp()
            reply = "Temperatures : \n"
            for core in self.botConfig.myCores:
                reply += core + " : " + ("%d " % temperatures[core]) + "°C \n"
            if numeric_result:
                return True, temperatures
            else:
                return True, reply
        except Exception:
            return False, "An error has occured on gettemp method"

    def getip(self):
        try:
            p = Popen('curl ifconfig.me', shell=True,
                      stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
            output = p.stdout.read()
            return True, str(ipaddress.ip_address(output.decode('UTF-8')))
        except Exception:
            return False, "Popen error or not a valid ipv4"

    def disks(self):
        """
        Returns your disks mountpoint and usages
        Code from pysysbot https://github.com/fabaff/pysysbot
        Thank you fabaff !
        """
        try:
            templ = "%-20s %8s %8s %8s %5s%% %s\n"
            disks = templ % ("Device", "Total", "Used",
                             "Free", "Use ", "Mount")
            for part in psutil.disk_partitions(all=False):
                usage = psutil.disk_usage(part.mountpoint)
                disks = disks + templ % (part.device,
                                         self._bytes2human(usage.total),
                                         self._bytes2human(usage.used),
                                         self._bytes2human(usage.free),
                                         int(usage.percent),
                                         part.mountpoint)
            return True, str(disks)
        except Exception:
            return False, ""

    def diskGraph(self):
        """
        Pie chart, where the slices will be ordered and
        plotted counter-clockwise
        """
        try:
            parts = psutil.disk_partitions(all=False)
            labels, sizes = [], []
            i, j = 0, 0

            if len(parts) == 1:  # case for 1 chart
                fig, axs = plt.subplots()
            elif len(parts) == 2:  # case for 2 charts, one over the other
                ncols, nrows = 1, 2
                fig, axs = plt.subplots(nrows, ncols)
            else:  # other case
                ncols, nrows = 1, 1
                while nrows * ncols < len(parts) + 1:
                    if ncols % nrows == 0:
                        ncols += 1
                    else:
                        nrows += 1
                fig, axs = plt.subplots(nrows, ncols)

            for part in parts:
                labels, sizes = [], []
                usage = psutil.disk_usage(part.mountpoint)
                labels.append("used : " + self._bytes2human(usage.used))
                labels.append("free : " + self._bytes2human(usage.free))
                sizes.append(int(usage.percent))
                sizes.append(100 - int(usage.percent))
                explode = (0.05, 0)  # only "explode" the 1st slice i.e. used

                if len(parts) == 1:  # case for 1 chart
                    axs.set_title(part.mountpoint,
                                  weight='bold',
                                  size='medium',
                                  position=(0.5, 1.1),
                                  horizontalalignment='center',
                                  verticalalignment='center')
                    axs.pie(sizes, labels=labels, autopct='%1.1f%%',
                            shadow=True, startangle=90, explode=explode)
                elif len(parts) >= 2:  # case for 2 charts or more
                    axs[i, j].set_title(part.mountpoint,
                                        weight='bold',
                                        size='medium',
                                        position=(0.5, 1.1),
                                        horizontalalignment='center',
                                        verticalalignment='center')
                    axs[i, j].pie(sizes, labels=labels, autopct='%1.1f%%',
                                  shadow=True, startangle=90, explode=explode)
                    axs[i, j].axis('equal')
                    # Equal aspect ratio ensures that pie
                    # is drawn as a circle.
                    if i == ncols - 1:
                        i = 0
                        j += 1
                    else:
                        i += 1
                    i, j, k = 0, 0, 0
                    while k < ncols * nrows:
                        try:
                            if not axs[i, j].get_title():
                                axs[i, j].set_visible(False)
                        except Exception:
                            print("error when blanking empty graphs")
                            i += 1
                        if i == ncols - 1:
                            i = 0
                            j += 1
                        else:
                            i += 1
                        k += 1

            fig.subplots_adjust(hspace=0.3)
            if os.path.isfile('/tmp/diskGraph.png'):
                os.remove('/tmp/diskGraph.png')
            plt.savefig('/tmp/diskGraph.png')
            plt.close()
            f = open('/tmp/diskGraph.png', 'rb')  # some file on local disk
            return True, (f, self.sendPicture)
        except Exception:
            return False, "Something went wrong on diskGraph"

    def testspeed(self):
        """ Return your internet speeds """
        st = speedtest.Speedtest()
        st.get_best_server()
        up = self._bytes2human(round(st.upload()))
        down = self._bytes2human(round(st.download()))
        return str(f"Up : {str(up)}bps\n \
                Down : {str(down)}bps")

# ############ Pihole #############

    def get_summary(self):
        self.pihole.refresh()
        summary = str('Status: ' + self.pihole.status + '\n'
                      + 'Domains being blocked: ' + self.pihole.domain_count
                      + '\n'
                      + 'Total Queries today: ' + self.pihole.queries + '\n'
                      + 'Ads blocked today: ' + self.pihole.blocked + '\n'
                      + 'Queries Blocked: ' + self.pihole.ads_percentage + '%'
                      + '\n'
                      + 'forwarded: ' + self.pihole.forwarded + '\n'
                      + 'cached: ' + self.pihole.cached + '\n'
                      + 'total_clients: ' + self.pihole.total_clients + '\n'
                      + 'unique_clients: ' + self.pihole.unique_clients + '\n'
                      + '\n')
        return summary

    def get_devices(self):
        self.pihole.refresh()
        m = 'Top devices : \n\n'
        for name, nb in self.pihole.top_devices.items():
            name, address = name.split('|')
            m += "{0} ({1}) : {2}\n".format(name, address, nb)
        return m

    def update_format(self):
        response = self.pihole.getVersion()
        component = ""
        if (response['core_update']
            or response['web_update']
           or response['FTL_update']):
            for name, value in response.items():
                if value == 'True':
                    component += " " + name.split("_")[0]
            return "An update is available for :" + component
        else:
            return "Your Pi-Hole is up to date !"

    def graph(self):
        datas = self.pihole.getGraphData()
        xads = list()
        xdomains = list()
        for i in datas['ads'].values():
            xads.append(i)
        for i in datas['domains'].values():
            xdomains.append(i)
        plt.figure()
        plt.subplot(211)
        plt.axis('auto')
        plt.xticks([])
        plt.title('Ads blocked')
        plt.plot(xads, "r", label="ads")
        plt.subplot(212)
        plt.axis('auto')
        plt.xticks([])
        plt.title('Domains requests')
        plt.plot(xdomains, "g", label="domains")

        if os.path.isfile('/tmp/pigraph.png'):
            os.remove('/tmp/pigraph.png')

        plt.savefig('/tmp/pigraph.png')
        plt.close()
        f = open('/tmp/pigraph.png', 'rb')  # some file on local disk
        return f

# ############ myWebSite #############

    def get_visits(self, dateToSearch):
        try:
            daily_match = re.match(r'\d{4}-\d{2}-\d{2}', dateToSearch)
            monthly_match = re.match(r'\d{4}-\d{2}', dateToSearch)
            isPicture = False
            if (dateToSearch.lower() == 'today'):
                d = date.today()
                isOK, result = self.ws_request_visits_by_date(d)
            elif bool(daily_match):
                d = datetime.strptime(dateToSearch, "%Y-%m-%d").date()
                isOK, result = self.ws_request_visits_by_date(d)
            elif bool(monthly_match):
                d = datetime.strptime(dateToSearch, "%Y-%m").date()
                isPicture = True
                isOK, result = self.ws_request_visits_by_month(d)

            if isPicture and isOK:
                return True, (result, self.sendPicture)
            elif isOK:
                return True, result
            else:
                raise Exception
        except Exception:
            return False, "Something went wrong on get_visits"

    def get_status(self):
        """
        request a website and check code to verify there is no issue
        """
        try:
            url = "https://www.unoeilsurlecode.fr/fr/"
            status_code = urllib.request.urlopen(url).getcode()
            ret = (f"The website {url} is online"
                   if status_code == 200
                   else f"There is an issue on the website {url}")
            return True, ret
        except Exception:
            return False, "Something went wrong on get_status"

    def _soap_client(self) -> SoapClient:
        client = SoapClient(
            location="https://WS.unoeilsurlecode.fr/unoeilsurlecodeWS.php",
            action="https://WS.unoeilsurlecode.fr/unoeilsurlecodeWS.php",
            namespace="https://WS.unoeilsurlecode.fr/unoeilsurlecodeWS.php",
            soap_ns='soap', ns=False
        )
        return client

    def _get_visitors_by_date(self, date: date) -> SimpleXMLElement:
        params = SimpleXMLElement(
            """<?xml version="1.0" encoding="UTF-8"?>
            <getVisitorByDate>
            <dateParam>
            """
            + date.__str__()
            + """</dateParam>
            </getVisitorByDate>"""
        )
        return params

    def _get_visitors_by_month(self, date: date) -> SimpleXMLElement:
        params = SimpleXMLElement(
            """<?xml version="1.0" encoding="UTF-8"?>
            <getAllVisitorsByMonth>
            <dateParam>"""
            + date.__str__()
            + """</dateParam>
            </getAllVisitorsByMonth>"""
        )
        return params

    def ws_request_visits_by_date(self, date: date):
        """
        call a webservice that returns visitors number by date
        """
        try:
            client = self._soap_client()
            params = self._get_visitors_by_date(date)
            response = client.call(
                'getVisitorByDate',
                params
            )
            visit = response.visitorsReturn
            if str(visit).__contains__('=>'):
                ret = str(visit).split('=>')[1]
            else:
                ret = "No result on this day"
            return True, ret
        except Exception:
            return False, "Something went wrong on ws_request_visits_by_date"

    def ws_request_visits_by_month(self, date: date):
        """
        call a webservice that returns a graph of visitors number by month
        """
        try:
            client = self._soap_client()
            response = client.call(
                'getAllVisitorsByMonth',
                self._get_visitors_by_month(date)
            )
            visits = str(response.visitorsReturn)
            _, visits = visits.split(' : ')
            list_x, list_y = [], []
            visits = visits.split(', ')
            for visitDay in visits:
                if str(visitDay) != "":
                    day = str(visitDay).split(' => ')[0]
                    visitsInDay = str(visitDay).split(' => ')[1]
                    if (day.isnumeric()
                       and visitsInDay.isnumeric()):
                        list_x.append(int(day))
                        list_y.append(int(visitsInDay))
            fig, ax = plt.subplots()
            ax.clear()
            ax.plot(list_x, list_y)
            ax.set_xlabel('day')
            ax.set_ylabel('visits on {}'.format(
                date.strftime("%B")
            ))
            ax.tick_params('both')
            ax.set_title(date.year)

            if os.path.isfile('/tmp/visitsByMonth.png'):
                os.remove('/tmp/visitsByMonth.png')

            plt.savefig('/tmp/visitsByMonth.png')
            plt.close()
            f = open('/tmp/visitsByMonth.png', 'rb')

            return True, (f, self.sendPicture)
        except Exception:
            return False, "Something went wrong on ws_request_visits_by_month"

# ############ Other #############

    def compile(self):
        # Done : auto set send alert Off when starting the build
        self.botConfig.setConfig('settings.ini', 'Alerts', 'sendAlerts', 1)
        buildScript = dict()
        buildScript['path'] = '/home/build/buildScript'
        buildScript['name'] = 'buildscript.sh'
        command_line = str("sudo -i -u build . "
                           + buildScript['path']
                           + "/"
                           + buildScript['name']
                           + " > /tmp/lastCompilation.log")
        p = Popen(command_line, shell=True, stdin=PIPE,
                  stderr=STDOUT, stdout=PIPE, close_fds=True)
        return p

    def restartBot(self):
        startupScript = '/usr/sbin/serverstatsbot.sh'
        self.botConfig.currentMenu = 'Restarting'
        command_line = str(startupScript + " start")
        args = shlex.split(command_line)
        pid = os.fork()
        if pid:
            subprocess.Popen(args)
            time.sleep(5)
            os._exit(1)
        else:
            os._exit(0)

    def compilStatus(self):
        command_line = str("tail -n5 /tmp/lastCompilation.log")
        p = Popen(command_line, shell=True, stdin=PIPE,
                  stderr=STDOUT, stdout=PIPE, close_fds=True)
        output = p.stdout.read()
        return output

    def restartEmby(self):
        command_line = str("systemctl restart emby-server")
        p = Popen(command_line, shell=True, stdin=PIPE,
                  stderr=STDOUT, stdout=PIPE, close_fds=True)
        output = p.stdout.read()
        return output

# ############ Settings #############

    def setgraphichours(self):
        try:
            firstDataTiming = self.botData.getFirstData()
            response = "first data in stats : " + \
                datetime.datetime \
                        .fromtimestamp(firstDataTiming) \
                        .strftime('%c')
            time_difference = round(time.time()) - firstDataTiming
            if time_difference < 60:
                msg = str(round(time_difference / 60)) + "seconds ago"
            if time_difference >= 60 and time_difference < 3600:
                msg = str(round(time_difference / 60)) + " minutes ago"
            if time_difference >= 3600:
                msg = str(round(time_difference / 3600)) + " hours ago"
            response += f"\nIt was {str(msg)}"
            return True, response
        except Exception:
            return False, "Something went wrong"

    def settinggraphichours(self, value):
        try:
            if float(value) < 240 * 3600:
                self.botConfig.setConfig('Graph',
                                         'length',
                                         round(float(value) * 3600))
                self.botConfig.loadSettings()
                return True, "Graphic hours set"
            else:
                raise ValueError()
        except ValueError:
            return False, "Please send a number of hours below 240"

    def settingmemth(self, value):
        try:
            if 0 < int(value) < 100:
                self.botConfig.setConfig('Graph',
                                         'memth',
                                         int(value))
                self.botConfig.loadSettings()
                return True, "Graph memth set!"
            else:
                raise ValueError()
        except ValueError:
            return False, "Please send a proper numeric value below 100"

    # cpu usage alert
    def settingcputh(self, value):
        try:
            if 0 < int(value) < 100:
                self.botConfig.setConfig('Graph',
                                         'cputh',
                                         int(value))
                self.botConfig.loadSettings()
                return True, "CPU usage threshold set"
            else:
                raise ValueError()
        except ValueError:
            return False, "Please send a proper numeric value below 100"

    def settingpollth(self, value):
        try:
            if 10 <= int(value) <= 300:
                self.botConfig.setConfig('Bot',
                                         'poll',
                                         int(value))
                self.botConfig.loadSettings()
                return True, "New polling interval set"
            else:
                raise ValueError()
        except ValueError:
            return False, "Please send a proper numeric value >= 10"

    def alerts(self):
        try:
            if self.botConfig.sendAlerts:
                self.botConfig.setConfig('Alerts', 'sendAlerts', 0)
            else:
                self.botConfig.setConfig('Alerts', 'sendAlerts', 1)
            if self.botConfig.sendAlerts:
                # disable_web_page_preview=True
                return True, "I'll send Alerts"
            else:
                # disable_web_page_preview=True
                return True, "I won't send Alerts"
        except Exception:
            return False, "Something went wrong"
