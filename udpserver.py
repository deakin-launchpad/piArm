
# WS server example

# import asyncio
import socket
from app import *
import json
import collections
import sys, getopt
from datetime import datetime

def start_server():
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    
    flag = True
    while flag:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        value = data.decode("ascii")

        if (value == "up"):
            up()
        elif (value == "down"):
            down()
        elif (value == "left"):
            left()
        elif (value == "right"):
            right()
        elif (value == "claw_open"):
            claw_open()
        elif (value == "claw_close"):
            claw_close()
        else:
            res = json.loads(value)
            if isinstance(res, collections.Mapping):
                if 'wrist_rotate' in res:
                    print ('Rotating wrist..')
                    claw_rotate(res["wrist_rotate"])
                if 'grab_strength' in res:
                    print ('Spreading claw..')
                    claw_spread(res["grab_strength"])

        print("Client [%s] < %s" % (datetime.now(), value))


UDP_IP = "127.0.0.1"
UDP_PORT = 5005

start_server()
