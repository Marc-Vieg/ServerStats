BOT UNDER MODIFICATION, FORKED FROM geekbeard/ServerStatsBot

# Server Manager Bot

A Telegram Bot:

* Menus :
   primary menu : Utils, Settings, Others
   
   * Utils :
   
      `Stats` -  gives summed statistics about memory and cpu usage \ disk \ processes (will improve)
      
      `BigGraph` - plots a graph of memory, temperatures, and cpu usage from the timeperiod specified in Settings/nd d heures graphique (yeah, some strings are in french, I'll translate strings
      
      `logwatch` send logwatch output line by line (telegram limits to 400 chars
      
      `temp` - Get Cores temperature (you have to specify the number of cores you have in botglobalvars.py
      
      `Raid` - cat /proc/mdstat for who have software raid
      
      `Disks` - get disks usages
      
      `Ip` - curl ifconfig.me to get your public IP
      
      
   * Settings : 
      `/setmem` - set memory threshold (%) to monitor and notify if memory usage goes above it
      
      `/setpoll` - set polling interval in seconds (higher than 10)
      
      `/setcpu` - set cppu threshold (%) to monitor and notify if cpu usage goes above it
      
      `Alerts On/Off` - Toggle if alerts will be sent when memeory or cpu usage % is bigger than threshold (on by default)
      
      `nd d heures graphique` - toggle the number of past hours to include in yout graphs
      
      
   * Others
      `Compile LineageOs` - I use it to toggle my buildscript for my lineageos Rom
      
      `Status` - only cat the logfile of my buildscript to know what it is doing
      
      `Restart Bot` - Restart bot with your personnal start|stop script
      



Example summary: [Gif](http://i.imgur.com/AhCvy9W.gifv)

![Bot](http://i.imgur.com/hXT0drx.png)



Example graph sent by bot: [Gif](http://i.imgur.com/anX7rJR.gifv)

![Graph](http://i.imgur.com/K8mG3aM.jpg?1)

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
 
 
# Other bot development
 
## Alfred
[http://alfredthebot.com](http://alfredthebot.com)
 
 
 CG
