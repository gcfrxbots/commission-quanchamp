from Settings import *
from subprocess import call
import urllib, urllib.request
import json
import socket
import os
import datetime
try:
    import xlsxwriter
    import xlrd
    import validators
except ImportError as e:
    print(e)
    raise ImportError(">>> One or more required packages are not properly installed! Run INSTALL_REQUIREMENTS.bat to fix!")
global settings

class socketConnection:
    def __init__(self):
        self.socketConn1 = socket.socket()
        self.socketConn2 = socket.socket()
        self.socketConn3 = socket.socket()
        self.socketConn4 = socket.socket()
        self.socketConn5 = socket.socket()

    def openSocket1(self):
        self.socketConn1.connect(("irc.chat.twitch.tv", int(settings['PORT'])))
        self.socketConn1.send(("PASS " + settings['BOT OAUTH'] + "\r\n").encode("utf-8"))
        self.socketConn1.send(("NICK " + settings['BOT NAME'] + "\r\n").encode("utf-8"))
        self.socketConn1.send(("JOIN #" + settings["CHANNEL 1 NAME"] + "\r\n").encode("utf-8"))
        return self.socketConn1

    def sendMessage1(self, message):
        print(message)
        messageTemp = "PRIVMSG #" + settings["CHANNEL 1 NAME"] + " : " + message
        self.socketConn1.send((messageTemp + "\r\n").encode("utf-8"))
        print("Sent to C1: " + messageTemp)

    def openSocket2(self):
        self.socketConn2.connect(("irc.chat.twitch.tv", int(settings['PORT'])))
        self.socketConn2.send(("PASS " + settings['BOT OAUTH'] + "\r\n").encode("utf-8"))
        self.socketConn2.send(("NICK " + settings['BOT NAME'] + "\r\n").encode("utf-8"))
        self.socketConn2.send(("JOIN #" + settings["CHANNEL 2 NAME"] + "\r\n").encode("utf-8"))
        return self.socketConn2

    def sendMessage2(self, message):
        print(message)
        messageTemp = "PRIVMSG #" + settings["CHANNEL 2 NAME"] + " : " + message
        self.socketConn2.send((messageTemp + "\r\n").encode("utf-8"))
        print("Sent to C2: " + messageTemp)

    def openSocket3(self):
        self.socketConn3.connect(("irc.chat.twitch.tv", int(settings['PORT'])))
        self.socketConn3.send(("PASS " + settings['BOT OAUTH'] + "\r\n").encode("utf-8"))
        self.socketConn3.send(("NICK " + settings['BOT NAME'] + "\r\n").encode("utf-8"))
        self.socketConn3.send(("JOIN #" + settings["CHANNEL 3 NAME"] + "\r\n").encode("utf-8"))
        return self.socketConn3

    def sendMessage3(self, message):
        print(message)
        messageTemp = "PRIVMSG #" + settings["CHANNEL 3 NAME"] + " : " + message
        self.socketConn3.send((messageTemp + "\r\n").encode("utf-8"))
        print("Sent to C3: " + messageTemp)
        
    def openSocket4(self):
        self.socketConn4.connect(("irc.chat.twitch.tv", int(settings['PORT'])))
        self.socketConn4.send(("PASS " + settings['BOT OAUTH'] + "\r\n").encode("utf-8"))
        self.socketConn4.send(("NICK " + settings['BOT NAME'] + "\r\n").encode("utf-8"))
        self.socketConn4.send(("JOIN #" + settings["CHANNEL 4 NAME"] + "\r\n").encode("utf-8"))
        return self.socketConn4

    def sendMessage4(self, message):
        print(message)
        messageTemp = "PRIVMSG #" + settings["CHANNEL 4 NAME"] + " : " + message
        self.socketConn4.send((messageTemp + "\r\n").encode("utf-8"))
        print("Sent to C4: " + messageTemp)
        
    def openSocket5(self):
        self.socketConn5.connect(("irc.chat.twitch.tv", int(settings['PORT'])))
        self.socketConn5.send(("PASS " + settings['BOT OAUTH'] + "\r\n").encode("utf-8"))
        self.socketConn5.send(("NICK " + settings['BOT NAME'] + "\r\n").encode("utf-8"))
        self.socketConn5.send(("JOIN #" + settings["CHANNEL 5 NAME"] + "\r\n").encode("utf-8"))
        return self.socketConn5

    def sendMessage5(self, message):
        print(message)
        messageTemp = "PRIVMSG #" + settings["CHANNEL 5 NAME"] + " : " + message
        self.socketConn5.send((messageTemp + "\r\n").encode("utf-8"))
        print("Sent to C5: " + messageTemp)

    def joinRoom(self, s):
        readbuffer = ""
        Loading = True

        while Loading:
            readbuffer = readbuffer + s.recv(1024).decode("utf-8")
            temp = readbuffer.split("\n")
            readbuffer = temp.pop()

            for line in temp:
                Loading = self.loadingComplete(line)

    def loadingComplete(self, line):
        if ("End of /NAMES list" in line):
            return False
        else:
            return True

class coreFunctions:
    def __init__(self):
        pass


    def getmoderators(self):
        moderators = []
        json_url = urllib.request.urlopen('http://tmi.twitch.tv/group/user/' + settings['CHANNEL'].lower() + '/chatters')
        data = json.loads(json_url.read())['chatters']
        mods = data['moderators'] + data['broadcaster']

        for item in mods:
            moderators.append(item)

        return moderators





chatConnection = socketConnection()
core = coreFunctions()

def initSetup():
    global settings


    # Create Folders
    if not os.path.exists('../Config'):
        buildConfig()
    if not os.path.exists('Resources'):
        os.makedirs('Resources')
        print("Creating necessary folders...")

    # Create Settings.xlsx
    loadedsettings = settingsConfig.settingsSetup(settingsConfig())
    settings = loadedsettings

    return settings


class timers:

    def __init__(self):
        self.timerActive = False
        self.timers = {}
        self.C1Cooldown = False
        self.C2Cooldown = False
        self.C3Cooldown = False
        self.C4Cooldown = False
        self.C5Cooldown = False


    def setTimer(self, name, duration):
        self.timerActive = True
        curTime = datetime.datetime.now()
        targetTime = curTime + datetime.timedelta(seconds=duration)
        self.timers[name] = targetTime

    def timerDone(self, timer):
        self.timers.pop(timer)
        print(timer + " timer complete.")
        if not self.timers:
            self.timerActive = False

        if timer == "1":
            self.C1Cooldown = False
        if timer == "2":
            self.C2Cooldown = False
        if timer == "3":
            self.C3Cooldown = False
        if timer == "4":
            self.C4Cooldown = False
        if timer == "5":
            self.C5Cooldown = False


timers = timers()
