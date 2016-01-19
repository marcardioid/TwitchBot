#!/usr/bin/env python3

import socket

con = socket.socket()


def connect(host, port):
    con.connect((host, port))
    return con


def disconnect():
    con.shutdown()
    con.close()


def receive():
    return con.recv(1024).decode("UTF-8")


def send_pong(msg):
    con.send(bytes("PONG {}\r\n".format(msg), "UTF-8"))


def send_message(chan, msg):
    con.send(bytes("PRIVMSG {} :{}\r\n".format(chan, msg), "UTF-8"))


def send_nick(nick):
    con.send(bytes("NICK {}\r\n".format(nick), "UTF-8"))


def send_pass(password):
    con.send(bytes("PASS {}\r\n".format(password), "UTF-8"))


def join_channel(chan):
    con.send(bytes("JOIN {}\r\n".format(chan), "UTF-8"))


def part_channel(chan):
    con.send(bytes("PART {}\r\n".format(chan), "UTF-8"))
