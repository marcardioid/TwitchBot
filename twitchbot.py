#!/usr/bin/env python3

import configparser
import irc
import re
import socket
from time import sleep

config = configparser.ConfigParser()
config.read("config.ini")
HOST = config["IRC"]["HOST"]
PORT = int(config["IRC"]["PORT"])
CHAN = config["IRC"]["CHAN"]
NICK = config["IRC"]["NICK"]
PASS = config["IRC"]["PASS"]

with open("wordfilter.txt", "r") as file:
    wordfilter = set([word.strip() for word in file.read().splitlines()])


def get_sender(msg):
    return msg.split('!', 1)[0][1:]


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + ' '
        i += 1
    return result.lstrip(':')


def parse_message(line):
    sender = get_sender(line[0])
    message = get_message(line)
    print(sender + ": " + message)
    if len(message) >= 1:
        words = message.split()
        options = {"!test": command_test,
                   "!derp": command_derp}
        if any(m.lower() in wordfilter for m in words):
            irc.timeout(CHAN, sender)
            print("SYS: TIMED OUT {}".format(sender.upper()))
            return
        if words[0] in options:
            options[words[0]]()


def command_test():
    irc.send_message(CHAN, "testing some stuff")


def command_derp():
    irc.send_message(CHAN, "derp yourself")


def main():
    irc.connect(HOST, PORT)
    irc.send_pass(PASS)
    irc.send_nick(NICK)
    irc.join_channel(CHAN)

    # irc.send_message(CHAN, ".me A WILD BOT JOINED THE CHAT!")
    print("SYS: A WILD BOT JOINED THE CHAT!")

    while True:
        try:
            data = irc.receive()
            data = re.split(r"[~\r\n]+", data)
            # data.pop()

            for line in data:
                line = str.rstrip(line)
                line = str.split(line)

                if len(line) >= 1:
                    if line[0] == "PING":
                        irc.send_pong(line[1])
                    if line[1] == "PRIVMSG":
                        parse_message(line)
            sleep(1 / (20 / 30))

        except socket.error:
            print("Socket died")
            break
        except socket.timeout:
            print("Socket timeout")
            break
        except (KeyboardInterrupt, SystemExit):
            break

    irc.disconnect()

    # irc.send_message(CHAN, ".me A WILD BOT LEFT THE CHAT!")
    print("SYS: A WILD BOT LEFT THE CHAT!")


if __name__ == "__main__":
    main()
