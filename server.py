
# WS server example

import asyncio
import websockets
from app import *
import json
import collections
import sys, getopt
from datetime import datetime

async def hello(websocket, path):
    value = await websocket.recv()
    
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
    # reply = 'Received: %s!'%(value)

    # await websocket.send(reply)
    # print('Sent: %s!'%(reply))

# def main(argv):
#     port = 8765

#     try:
#         opts, args = getopt.getopt(argv,"hp:",["help","port="])
#     except getopt.GetoptError:
#         print ('server.py -p <PORT>')
#         sys.exit(2)

#     for opt, arg in opts:
#         if opt in ('-h', '--help'):
#             print ('server.py -p <PORT>')
#             sys.exit()
#         elif opt in ("-p", "--port"):
#             port = arg
#     start_server = websockets.serve(hello, "localhost", port)
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()

port = 8765
start_server = websockets.serve(hello, "localhost", port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
