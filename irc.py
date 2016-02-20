#!/usr/bin/env python3

import socket

con = socket.socket()


def connect(host, port):
    """Create a connection to IRC and return it."""
    con.connect((host, port))
    return con


def disconnect():
    """Disconnect from IRC."""
    con.shutdown(socket.SHUT_RDWR)
    con.close()


def receive():
    """Receive a message from IRC."""
    return con.recv(1024).decode("UTF-8")


def send_pong(msg):
    """Send PONG to IRC."""
    con.send(bytes("PONG {}\r\n".format(msg), "UTF-8"))


def send_message(chan, msg):
    """Send PRIVMSG to IRC."""
    con.send(bytes("PRIVMSG {} :{}\r\n".format(chan, msg), "UTF-8"))


def send_nick(nick):
    """Send NICK to IRC."""
    con.send(bytes("NICK {}\r\n".format(nick), "UTF-8"))


def send_pass(password):
    """Send PASS to IRC."""
    con.send(bytes("PASS {}\r\n".format(password), "UTF-8"))


def join_channel(chan):
    """Join IRC channel."""
    con.send(bytes("JOIN {}\r\n".format(chan), "UTF-8"))


def part_channel(chan):
    """Leave IRC channel."""
    con.send(bytes("PART {}\r\n".format(chan), "UTF-8"))


def ban(chan, user):
    """Ban user."""
    send_message(chan, ".ban {}".format(user))


def timeout(chan, user, time=1):
    """Timeout user."""
    send_message(chan, ".timeout {} {}".format(user, time))
