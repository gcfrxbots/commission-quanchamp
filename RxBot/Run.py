from threading import Thread
from CustomCommands import CustomCommands, commands_CustomCommands
from Initialize import *
import random

settings = initSetup()

customcmds = CustomCommands()




class runMiscControls:

    def __init__(self):
        pass

    def getUser(self, line):
        seperate = line.split(":", 2)
        user = seperate[1].split("!", 1)[0]
        return user

    def getMessage(self, line):
        seperate = line.split(":", 2)
        message = seperate[2]
        return message

    def formatTime(self):
        return datetime.datetime.today().now().strftime("%I:%M")


def runcommand(command, cmdArguments, user, mute):
    commands = {**commands_CustomCommands}
    cmd = None
    arg1 = None
    arg2 = None

    for item in commands:
        if item == command:
            if commands[item][0] == "MOD":  # MOD ONLY COMMANDS:
                if (user in core.getmoderators()):
                    cmd = commands[item][1]
                    arg1 = commands[item][2]
                    arg2 = commands[item][3]
                else:
                    chatConnection.sendMessage("You don't have permission to do this.")
                    return
            elif commands[item][0] == "STREAMER":  # STREAMER ONLY COMMANDS:
                if (user == settings['CHANNEL']):
                    cmd = commands[item][1]
                    arg1 = commands[item][2]
                    arg2 = commands[item][3]
                else:
                    chatConnection.sendMessage("You don't have permission to do this.")
                    return
            else:
                cmd = commands[item][0]
                arg1 = commands[item][1]
                arg2 = commands[item][2]
            break
    if not cmd:
        return

    #try:  # Run all commands as a try/except, so the bot doesn't crash if one bot errors out.
    output = eval(cmd + '(%s, %s)' % (arg1, arg2))
    #except Error as e:
        # print("Error running the command %s with the args %s" % (command, cmdArguments))
        # print(e)
    #else:
    if not output:
        return

    chatConnection.sendMessage(user + " >> " + output)


def watchChannel1():
    success = False
    s = None
    while not success:
        try:
            s = chatConnection.openSocket1()
            chatConnection.joinRoom(s)
            success = True
        except Exception as e:
            time.sleep(1)
            s = None
            chatConnection.socketConn1.close()
            chatConnection.socketConn1 = socket.socket()
            pass
    print(">> Connection to %s successful" % settings["CHANNEL 1 NAME"])
    readbuffer = ""
    while True:
        readbuffer = readbuffer + s.recv(1024).decode("utf-8")
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            if "PING" in line:
                s.send(bytes("PONG :tmi.twitch.tv\r\n".encode("utf-8")))
            else:
                # All these things break apart the given chat message to make things easier to work with.
                user = misc.getUser(line)
                message = str(misc.getMessage(line))
                command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
                cmdArguments = message.replace(command or "\r" or "\n", "").strip()
                print(("CHANNEL1 - (" + misc.formatTime() + ")>> " + user + ": " + message))

                if settings["TRIGGER MESSAGE"] in message and not timers.C1Cooldown:
                    time.sleep(random.uniform(1, 4))
                    chatConnection.sendMessage1(settings["TRIGGER MESSAGE"])
                    timers.setTimer("1", settings["COOLDOWN"])
                    timers.C1Cooldown = True


def watchChannel2():
    success = False
    s = None
    while not success:
        try:
            s = chatConnection.openSocket2()
            chatConnection.joinRoom(s)
            success = True
        except Exception as e:
            time.sleep(1)
            s = None
            chatConnection.socketConn2.close()
            chatConnection.socketConn2 = socket.socket()
            pass
    print(">> Connection to %s successful" % settings["CHANNEL 2 NAME"])
    readbuffer = ""
    while True:
        readbuffer = readbuffer + s.recv(1024).decode("utf-8")
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            if "PING" in line:
                s.send(bytes("PONG :tmi.twitch.tv\r\n".encode("utf-8")))
            else:
                # All these things break apart the given chat message to make things easier to work with.
                user = misc.getUser(line)
                message = str(misc.getMessage(line))
                command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
                cmdArguments = message.replace(command or "\r" or "\n", "").strip()
                print(("CHANNEL2 - (" + misc.formatTime() + ")>> " + user + ": " + message))

                if settings["TRIGGER MESSAGE"] in message and not timers.C2Cooldown:
                    time.sleep(random.uniform(1, 4))
                    chatConnection.sendMessage2(settings["TRIGGER MESSAGE"])
                    timers.setTimer("2", settings["COOLDOWN"])
                    timers.C2Cooldown = True


def watchChannel3():
    success = False
    s = None
    while not success:
        try:
            s = chatConnection.openSocket3()
            chatConnection.joinRoom(s)
            success = True
        except Exception as e:
            time.sleep(1)
            s = None
            chatConnection.socketConn3.close()
            chatConnection.socketConn3 = socket.socket()
            pass
    print(">> Connection to %s successful" % settings["CHANNEL 3 NAME"])
    readbuffer = ""
    while True:
        readbuffer = readbuffer + s.recv(1024).decode("utf-8")
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            if "PING" in line:
                s.send(bytes("PONG :tmi.twitch.tv\r\n".encode("utf-8")))
            else:
                # All these things break apart the given chat message to make things easier to work with.
                user = misc.getUser(line)
                message = str(misc.getMessage(line))
                command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
                cmdArguments = message.replace(command or "\r" or "\n", "").strip()
                print(("CHANNEL3 - (" + misc.formatTime() + ")>> " + user + ": " + message))

                if settings["TRIGGER MESSAGE"] in message and not timers.C3Cooldown:
                    time.sleep(random.uniform(1, 4))
                    chatConnection.sendMessage3(settings["TRIGGER MESSAGE"])
                    timers.setTimer("3", settings["COOLDOWN"])
                    timers.C3Cooldown = True



def console():  # Thread to handle console input
    while True:
        consoleIn = input("")

        command = ((consoleIn.split(' ', 1)[0]).lower()).replace("\r", "")
        cmdArguments = consoleIn.replace(command or "\r" or "\n", "").strip()
        # Run the commands function
        if command:
            if command[0] == "!":
                runcommand(command, cmdArguments, "CONSOLE", True)

            if command.lower() in ["quit", "exit", "leave", "stop", "close"]:
                print("Shutting down")
                os._exit(1)

def tick():
    prevTime = datetime.datetime.now()
    while True:
        time.sleep(0.4)

        if timers.timerActive:
            for timer in timers.timers:
                if datetime.datetime.now() > timers.timers[timer]:
                    timers.timerDone(timer)
                    break


if __name__ == "__main__":
    misc = runMiscControls()

    t1 = Thread(target=watchChannel1)
    t2 = Thread(target=watchChannel2)
    t3 = Thread(target=watchChannel3)
    t4 = Thread(target=console)
    t5 = Thread(target=tick)

    t1.start()
    time.sleep(0.5)
    t2.start()
    time.sleep(0.5)
    t3.start()
    time.sleep(0.5)
    t4.start()
    t5.start()

