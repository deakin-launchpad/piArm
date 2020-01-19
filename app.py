from flask import Flask, request

import re
import piarm
import sys

app = Flask(__name__)

'''
PiArm Connection between raspberrypi and servo shield through serial port.
Use dmesg|grep tty to know which serial port that is connected
'''
print('Connecting robot arm')
robot = piarm.PiArm()
robot.connect("/dev/ttyAMA0")

# Array to update the servo position
right_arm = {
    1: 750,
    2: 500,
    3: 700,
    4: 700,
    5: 200,
    6: 0
    }

__left_arm_starting_index__ = 50
# Default move step for servo
servo_move_step = 50
left_arm = {}

#####
# TODO: Loop through 1 to 6 and set default value as 500 for everything
#####


#####

# Print a message
def log(message):
    print(message, file = sys.stdout)

# Function to write/update the current servo position
def write_servo():
    if robot.alive:
        for servoid in range (1,7):
            robot.servoWrite(servoid, right_arm[servoid], 1000)
            # print("Writing to Servo ID {} position:".format(servoid),right_arm[servoid])

# Default position or reset position if the position value reached max or out of range
@app.route('/default')
def default():           
    right_arm = {
        1: 750,
        2: 500,
        3: 700,
        4: 700,
        5: 200,
        6: 0,
        }
    write_servo()
    log('default')
    return 'default'

           
# Extend arm for servo 3, 4, 5 to given value
# @app.route('/up')
def extend_arm(value):
    
    right_arm[5] = value
    right_arm[4] = value
    right_arm[3] = value
    
    write_servo()
    log('Extending arm to given value')

# Flex arm down for servo 3, 4, 5
@app.route('/default_flex_arm')
def default_flex_arm():
    if right_arm[5] - servo_move_step in range(101, 999):
        right_arm[5] -= servo_move_step
    if right_arm[4] + servo_move_step in range(1, 999):
        right_arm[4] += (servo_move_step - 20)
    if right_arm[3] - servo_move_step in range(400, 970):
        right_arm[3] -= servo_move_step
    
    write_servo()
    log('default_flex_arm')
    return 'default_flex_arm'

# Rotate servo 6 to given value
def rotate(value):
    right_arm[6] = value

    write_servo()
    log('Rotate robot to given value')

# Rotate servo 2 to given value
# @app.route('/claw_rotate')
def claw_rotate(value):
    
    right_arm[2] = value

    write_servo()
    log('Claw rotate to given value')
    # return 'Claw rotate to given value'

# Spread claw to given value
# @app.route('/close')
def claw_spread(value):
    right_arm[1] = value
    
    write_servo()
    log('Spread claw to given value')

# Set default speed of each servo motor
@app.route('/speed')
def set_speed():
    # TODO: Make sure the speed is a positive integer value.
    # TODO: Make sure that speed is no greater than 100.
        
    try:
        temp = int(request.args['speed'])
        if temp < 1:
            print("invalid")
        elif temp < 100:
            print("valid")
            servo_move_step = temp
        else:
            return 'Speed can\'t be greater than 99'

    except ValueError:
        log('Invalid value')
        return 'Invalid value'

    # current = servo_move_step  
    # servo_move_step = request.args['speed']
    # log('speed changed to:' + temp)
    # log('current speed:'+ str(current))
    # log('current speed:'+ temp)
    return 'Current speed:' + str(servo_move_step) + ', new speed to:' + str(temp)


if __name__ == '__main__':
    print("starting server",file=sys.stdout)
    log("Starting robot")
    print(right_arm)

    app.run(debug=True, host='0.0.0.0', port=2000)
