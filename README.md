BOT UNDER MODIFICATION, FORKED FROM geekbeard/ServerStatsBot

# Server Stats Bot

A Telegram Bot to watch your server or personal computer.

### Utils 
	Stats 	-> returns uptime, memory and cpu usage 
    Temp 	-> returns actual temperatures of your processor
    speedtest -> will test your internet bandwith
    Big Graph -> will plot you a beautiful graphic of your server's stats (with adjustable time)
    logwatch -> will send you the [logwatch](https://sourceforge.net/projects/logwatch/)'s report
	Raid 	-> will give you the status of your Raid Array (content of /proc/mdstats)
    Disk 	-> your disks mountpoint and usages 
    IP 		-> Your external IP
    
### Settings
	setmem, setcpu, setpoll -> 	let you choose an alert threshold for usages of you cpu and memory 
    							or your processor temperature
    Alerts On/Off 	-> tell the bot to send alerts or not
    Graph Lenght 	-> choose the maximum time to show in Big Graph (decimal friendly, actualy code limited to 240 hours max)

### Others
	I use this menu to compile LineageOs update for my phone, it's linked to my build script and his logfile. (Compile LineagOs and Status buttons)
    
    Restart Bot to restart the bot


    
***

Example summary: [Gif](http://i.imgur.com/AhCvy9W.gifv)

![Bot](https://github.com/CobayeGunther/ServerStatsBot/blob/staging/docs/lastHour.jpg)
![Bot](https://github.com/CobayeGunther/ServerStatsBot/blob/staging/docs/last2Hours.jpg)



# Usage

## Requirements 

* Python 3+
* [Telepot](https://github.com/nickoala/telepot)
* [Psutil](https://github.com/giampaolo/psutil)
    * Make sure to install it for Python 3+
    * In order to make sure that `pip` installs packages for the 3+ version:
        * `curl -O https://bootstrap.pypa.io/get-pip.py`
        * `sudo python3 get-pip.py`
        * After that `pip install psutil`
        * Also Stackoverflow question about that [here](http://stackoverflow.com/questions/11268501/how-to-use-pip-with-python-3-x-alongside-python-2-x)
* [matplotlib](http://matplotlib.org/)
    * `sudo apt-get install python3-matplotlib`
* [speedtest-cli](https://github.com/sivel/speedtest-cli)
    * `sudo pip install speedtest-cli`
* Bot key & `tokens.py`
    * Hide all the keys and admin variables in `tokens.py`. Use it only for sensitive variables. Avoid creating functions not to clutter the namespaces through the import.
    * Get a key from the [Bot Father](https://telegram.me/BotFather)
    * Clone that repo
    * In the folder with the cloned repo create a file `tokens.py`
       * It's added to the `.gitignore` so you don't commit your own (and I don't commit mine:)
    * In that file put a string variable `telegrambot` which equals your key
       * For example: `telegrambot = "000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"`
   
## Running the bot

`python3 servstatsbot.py`

## Running the bot as "daemon"

* See included file in the repo: `servstatsbot.conf`
    * Open it and edit the path as mentiond in the comments there
* Place that file in `/etc/init/`
* Start the "daemon" with: `start servstatsbot`
    * You can start|stop|restart
    * If bot crashes it'll be automatically restarted
    * It will also start after reboot

## Setting an admin

You have to set a variable `adminchatid` in `tokens.py` to be equal your chat_id or multiple chat_id (if more people will use your bot).
For example:

* `adminchatid = [443355]`
* `adminchatid = [443355, 55667788, 99884433]`

I will reimplement this differently later.
        
 
# PLEASE CONTRIBUTE :)
I got the original code from geekbeard/ServerStatsBot and adpted it to my personnal usage, please feel free to thank him and fork your own version !


pihole work in progress thanks to mnk400/pihole-info
 
 
# Other bot development
 
## Alfred
[http://alfredthebot.com](http://alfredthebot.com)
 
 
 CG

