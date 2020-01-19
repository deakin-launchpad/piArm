
# WS server example

# import asyncio
import socket
import piarm
from app import *
from arm import Arm
import json
import collections
import sys, getopt
from datetime import datetime
from threading import _start_new_thread

IP_ADDR = "127.0.0.1"
PORT = 8765

RIGHT_ARM_INDEX = 0
LEFT_ARM_INDEX = 50

decoder = json.JSONDecoder()

robot = piarm.PiArm()
robot.connect("/dev/ttyAMA0")

DEFAULT_RESPONSE = "ack".encode()
CLIENT_ERROR = "CLIENT error".encode()
SERVER_ERROR = "SERVER error".encode()

ARMS = {
    'Right': Arm(robot, RIGHT_ARM_INDEX),
    'Left': Arm(robot, LEFT_ARM_INDEX)
}

def client_thread(conn, robot_arm):
    # conn.send(":smile:")
    while True:
        try:
            data = conn.recv(1024) # buffer size is 1024 bytes
        except socket.timeout:
            print('Socket timed out')
            break

        # This check will ensure that empty streams, generally caused by
        # unorderly terminating a socket connection at the client side
        # is handled gracefully.
        if len(data) == 0:
            print('No data to read from stream')
            break

        value = data.decode()
        print("Client [%s] < %s" % (datetime.now(), value))

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
            value = value.lstrip()
            while value:
                try:
                    res, index = decoder.raw_decode(value)
                    value = value[index:].lstrip()

                    if isinstance(res, collections.Mapping):
                        if 'wrist_rotate' in res:
                            print ('Rotating wrist..')
                            robot_arm.claw_rotate(res["wrist_rotate"])
                        if 'grab_strength' in res:
                            print ('Spreading claw..')
                            robot_arm.claw_spread(res["grab_strength"])
                except json.decoder.JSONDecodeError:
                    # Will only happen in the end. Can be useless so break.
                    conn.send(CLIENT_ERROR)
                    break
        
        conn.send(DEFAULT_RESPONSE)

    print('Closing client connection')
    conn.close()

def determine_handedness(conn):
    try:
        data = conn.recv(1024) # buffer size is 1024 bytes
    except socket.timeout:
        print('Socket timed out')
        return

    # This check will ensure that empty streams, generally caused by
    # unorderly terminating a socket connection at the client side
    # is handled gracefully.
    if len(data) == 0:
        print('No data to read from stream')
        return

    value = data.decode()
    print("Client [%s] < %s" % (datetime.now(), value))

    value = value.lstrip()
    while value:
        try:
            res, index = decoder.raw_decode(value)
            value = value[index:].lstrip()

            if isinstance(res, collections.Mapping):
                if 'handedness' in res:
                    return res["handedness"]
        except json.decoder.JSONDecodeError:
            # Will only happen in the end. Can be useless so break.
            conn.send(CLIENT_ERROR)
            return


def start_server():
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_STREAM) # TCP

    socket.setdefaulttimeout(5) # Timeout in seconds
    sock.bind((IP_ADDR, PORT))
    sock.listen(1)
    print("Listening for connections..")

    # right_arm = Arm(robot, RIGHT_ARM_INDEX)

    while True:
        conn, addr = sock.accept()
        print ('Connection address:', addr)
        handedness = determine_handedness(conn)
        print ('Handedness: %s' % handedness)

        if (handedness):
            required_arm = ARMS[handedness]
            _start_new_thread(client_thread, (conn, required_arm,))

    sock.close()

start_server()
