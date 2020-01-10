from flask import Flask

import re
import piarm
import sys

app = Flask(__name__)


'''
PiArm Connection between raspberrypi and servo shield through serial port.
Use dmesg|grep tty to know which serial port that is connected
'''
robot = piarm.PiArm()
robot.connect("/dev/ttyAMA0")


#array to update the servo position
servo_position = {
    1: 750,
    2: 500,
    3: 700,
    4: 700,
    5: 200,
    6: 800    
    }

#default move step for servo
servo_move_step = 50

#print a message
def log(message):
    print(message,file=sys.stdout)

'''
def moveArm(command):
    return command

def initialiseRobot():
    
    log('trying to move arm')    
    #robot.servoWrite(1,750, 1000)
'''

#function to write/update the current servo position
def write_servo():
    if robot.alive:
        for servoid in range (1,7):
            robot.servoWrite(servoid, servo_position[servoid], 1500)

'''
@app.route('/')
def index():
    
    #initialiseRobot()
    
    return 'hello world'
'''



#Move Arm Up for servo 3,4,5
@app.route('/up')
def up():
    if servo_position[5] + servo_move_step in range(101, 999):
        servo_position[5] += servo_move_step
    if servo_position[4] - servo_move_step in range(1, 999):
        servo_position[4] -= servo_move_step
    if servo_position[3] + servo_move_step in range(400, 970):
        servo_position[3] += servo_move_step
    
    write_servo()
    log('up')
    return 'move up'


@app.route('/down')
def down():
    if servo_position[5] - servo_move_step in range(101, 999):
        servo_position[5] -= servo_move_step
    if servo_position[4] + servo_move_step in range(1, 999):
        servo_position[4] += (servo_move_step - 20)
    if servo_position[3] - servo_move_step in range(400, 970):
        servo_position[3] -= servo_move_step
    
    write_servo()
    log('down')
    return 'move down'

#Claw closed
@app.route('/close')
def claw_close():
    if servo_position[1] + servo_move_step in range(144, 999):
        servo_position[1] += servo_move_step
    
    write_servo()
    log('close')    
    return 'claw closed'
    
#Claw open
@app.route('/open')
def claw_open():
    
    if servo_position[1] - servo_move_step in range(144, 999):
        servo_position[1] -= servo_move_step
        
    write_servo()
    log('open')
    return 'claw open'

if __name__ == '__main__':
    print("starting server",file=sys.stdout)
    log("Starting robot")
    #initialiseRobot()
    
    
    log("After initialise")
    app.run(debug=True, host='0.0.0.0', port=2000)

    

