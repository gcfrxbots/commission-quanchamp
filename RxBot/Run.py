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

    def isInt(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def duelLogic(self, message):
        msgArgs = message.split()[-1]

        if not self.isInt(msgArgs):  # Its a string, deny it
            return "!deny"
        else:
            value = int(msgArgs)
            if value > settings["DUEL LIMIT"]:
                return "!deny"

        return "!accept"



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
    print(">> Connection to %s successful" % settings["CHANNEL NAME"])
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
                message = str(misc.getMessage(line)).strip().replace("\r", "")
                command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
                cmdArguments = message.replace(command or "\r" or "\n", "").strip()
                print(("(" + misc.formatTime() + ")>> " + user + ": " + message))
                print("!duel @%s" % settings["BOT NAME"])
                if settings["TRIGGER MESSAGE 1"] in message and not timers.C1Cooldown:
                    print("%s Detected - Waiting %s seconds before sending response." % (settings["TRIGGER MESSAGE 1"], str(settings["DELAY 1"])))
                    time.sleep(settings["DELAY 1"] + 1)  # Adds an extra second just in case
                    chatConnection.sendMessage1(settings["RESPONSE 1"])
                    timers.setTimer("1", settings["COOLDOWN 1"])
                    timers.C1Cooldown = True

                elif settings["TRIGGER MESSAGE 2"] in message and not timers.C2Cooldown:
                    print("%s Detected - Waiting %s seconds before sending response." % (settings["TRIGGER MESSAGE 2"], str(settings["DELAY 2"])))
                    time.sleep(settings["DELAY 2"] + 1)  # Adds an extra second just in case
                    chatConnection.sendMessage1(settings["RESPONSE 2"])
                    timers.setTimer("2", settings["COOLDOWN 2"])
                    timers.C2Cooldown = True


                elif ("!duel @%s" % settings["BOT NAME"]).lower() in message.lower() and not timers.C3Cooldown:
                    print("!duel Detected - Waiting %s seconds before sending response." % str(settings["DUEL DELAY"]))
                    time.sleep(settings["DUEL DELAY"] + 1)  # Adds an extra second just in case
                    chatConnection.sendMessage1(misc.duelLogic(message))
                    timers.setTimer("3", settings["DUEL COOLDOWN"])
                    timers.C3Cooldown = True


                elif timers.C1Cooldown:
                    print("Still on cooldown, not sending anything yet")
                elif timers.C2Cooldown:
                    print("Still on cooldown, not sending anything yet")
                elif timers.C3Cooldown:
                    print("Still on cooldown, not sending anything yet")

# def watchChannel2():
#     success = False
#     s = None
#     while not success:
#         try:
#             s = chatConnection.openSocket2()
#             chatConnection.joinRoom(s)
#             success = True
#         except Exception as e:
#             time.sleep(1)
#             s = None
#             chatConnection.socketConn2.close()
#             chatConnection.socketConn2 = socket.socket()
#             pass
#     print(">> Connection to %s successful" % settings["CHANNEL 2 NAME"])
#     readbuffer = ""
#     while True:
#         readbuffer = readbuffer + s.recv(1024).decode("utf-8")
#         temp = readbuffer.split("\n")
#         readbuffer = temp.pop()
#         for line in temp:
#             if "PING" in line:
#                 s.send(bytes("PONG :tmi.twitch.tv\r\n".encode("utf-8")))
#             else:
#                 # All these things break apart the given chat message to make things easier to work with.
#                 user = misc.getUser(line)
#                 message = str(misc.getMessage(line)).strip().replace("\r", "")
#                 command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
#                 cmdArguments = message.replace(command or "\r" or "\n", "").strip()
#                 print(("CHANNEL2 - (" + misc.formatTime() + ")>> " + user + ": " + message))
#
#                 if settings["TRIGGER MESSAGE"] == message and not timers.C2Cooldown:
#                     time.sleep(random.uniform(10, 30))
#                     chatConnection.sendMessage2(settings["TRIGGER MESSAGE"])
#                     timers.setTimer("2", settings["CHANNEL 2 COOLDOWN"])
#                     timers.C2Cooldown = True
#
#
# def watchChannel3():
#     success = False
#     s = None
#     while not success:
#         try:
#             s = chatConnection.openSocket3()
#             chatConnection.joinRoom(s)
#             success = True
#         except Exception as e:
#             time.sleep(1)
#             s = None
#             chatConnection.socketConn3.close()
#             chatConnection.socketConn3 = socket.socket()
#             pass
#     print(">> Connection to %s successful" % settings["CHANNEL 3 NAME"])
#     readbuffer = ""
#     while True:
#         readbuffer = readbuffer + s.recv(1024).decode("utf-8")
#         temp = readbuffer.split("\n")
#         readbuffer = temp.pop()
#         for line in temp:
#             if "PING" in line:
#                 s.send(bytes("PONG :tmi.twitch.tv\r\n".encode("utf-8")))
#             else:
#                 # All these things break apart the given chat message to make things easier to work with.
#                 user = misc.getUser(line)
#                 message = str(misc.getMessage(line)).strip().replace("\r", "")
#                 command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
#                 cmdArguments = message.replace(command or "\r" or "\n", "").strip()
#                 print(("CHANNEL3 - (" + misc.formatTime() + ")>> " + user + ": " + message))
#
#                 if settings["TRIGGER MESSAGE"] == message and not timers.C3Cooldown:
#                     time.sleep(random.uniform(10, 30))
#                     chatConnection.sendMessage3(settings["TRIGGER MESSAGE"])
#                     timers.setTimer("3", settings["CHANNEL 3 COOLDOWN"])
#                     timers.C3Cooldown = True
#
# def watchChannel4():
#     success = False
#     s = None
#     while not success:
#         try:
#             s = chatConnection.openSocket4()
#             chatConnection.joinRoom(s)
#             success = True
#         except Exception as e:
#             time.sleep(1)
#             s = None
#             chatConnection.socketConn4.close()
#             chatConnection.socketConn4 = socket.socket()
#             pass
#     print(">> Connection to %s successful" % settings["CHANNEL 4 NAME"])
#     readbuffer = ""
#     while True:
#         readbuffer = readbuffer + s.recv(1024).decode("utf-8")
#         temp = readbuffer.split("\n")
#         readbuffer = temp.pop()
#         for line in temp:
#             if "PING" in line:
#                 s.send(bytes("PONG :tmi.twitch.tv\r\n".encode("utf-8")))
#             else:
#                 # All these things break apart the given chat message to make things easier to work with.
#                 user = misc.getUser(line)
#                 message = str(misc.getMessage(line)).strip().replace("\r", "")
#                 command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
#                 cmdArguments = message.replace(command or "\r" or "\n", "").strip()
#                 print(("CHANNEL4 - (" + misc.formatTime() + ")>> " + user + ": " + message))
#
#                 if settings["TRIGGER MESSAGE"] == message and not timers.C4Cooldown:
#                     time.sleep(random.uniform(10, 30))
#                     chatConnection.sendMessage4(settings["TRIGGER MESSAGE"])
#                     timers.setTimer("4", settings["CHANNEL 4 COOLDOWN"])
#                     timers.C4Cooldown = True
#
# def watchChannel5():
#     success = False
#     s = None
#     while not success:
#         try:
#             s = chatConnection.openSocket5()
#             chatConnection.joinRoom(s)
#             success = True
#         except Exception as e:
#             time.sleep(1)
#             s = None
#             chatConnection.socketConn5.close()
#             chatConnection.socketConn5 = socket.socket()
#             pass
#     print(">> Connection to %s successful" % settings["CHANNEL 5 NAME"])
#     readbuffer = ""
#     while True:
#         readbuffer = readbuffer + s.recv(1024).decode("utf-8")
#         print(readbuffer)
#         temp = readbuffer.split("\n")
#         readbuffer = temp.pop()
#         for line in temp:
#             if "PING" in line:
#                 s.send(bytes("PONG :tmi.twitch.tv\r\n".encode("utf-8")))
#             else:
#                 # All these things break apart the given chat message to make things easier to work with.
#                 user = misc.getUser(line)
#                 message = str(misc.getMessage(line)).strip().replace("\r", "")
#                 command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
#                 cmdArguments = message.replace(command or "\r" or "\n", "").strip()
#                 print(("CHANNEL5 - (" + misc.formatTime() + ")>> " + user + ": " + message))
#
#                 if settings["TRIGGER MESSAGE"] == message and not timers.C5Cooldown:
#                     time.sleep(random.uniform(10, 30))
#                     chatConnection.sendMessage5(settings["TRIGGER MESSAGE"])
#                     timers.setTimer("5", settings["CHANNEL 5 COOLDOWN"])
#                     timers.C5Cooldown = True



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
    # t2 = Thread(target=watchChannel2)
    # t3 = Thread(target=watchChannel3)
    # t4 = Thread(target=watchChannel4)
    # t5 = Thread(target=watchChannel5)
    t6 = Thread(target=console)
    t7 = Thread(target=tick)

    t1.start()
    # t2.start()
    # time.sleep(1)
    # t3.start()
    # time.sleep(1)
    # t4.start()
    # time.sleep(1)
    # t5.start()
    # time.sleep(1)
    t6.start()
    t7.start()

