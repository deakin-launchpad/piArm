import re
import piarm
from time import sleep

import pigpio
import curses

class keyboard(object):
    def __init__(self):
        self.servo_POS_error = False
        self.keypress_status = False
        self.step = 50
        self.servo_position = {
                 1: 750,
                 2: 500,
                 3: 700,
                 4: 700,
                 5: 200,
                 6: 800,
            }
        self.button_status = {
                     0: 0,
                     1: 0,
                     2: 0,
                     3: 0,
                     4: 0,
                     5: 0,
                     6: 0
            }
    
    pi = pigpio.pi()
    
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    
    def listen(self):
        while True:
            if robot.alive:
                for ID in range(1, 7):
                    #self.servo_position[ID] = 500
                    self.servo_position = {
                                    1: 750,
                                    2: 500,
                                    3: 700,
                                    4: 700,
                                    5: 200,
                                    6: 800,
                                    }
                    
                    robot.servoWrite(ID, self.servo_position[ID], 1500)
            else:
                print('Comm port is not conected')
                
            for Char, status in self.button_status.items():
                
                Char = screen.getch()
            
                if Char == ord('w'):
                    if self.servo_position[5] - self.step in range(101, 999):
                        self.servo_position[5] -= self.step
                    if self.servo_position[4] + self.step in range(1, 999):
                        self.servo_position[4] += (self.step + 20)
                    if self.servo_position[3] - self.step in range(400, 970):
                        self.servo_position[3] -= (self.step + 40)
                    print ('Up')
                
                if Char == ord('a'):
                    if self.servo_position[6] - self.step in range(10, 980):
                        self.servo_position[6] += self.step
                    print('rotate left')
                
                if Char == ord('s'):
                    if self.servo_position[5] + self.step in range(101, 999):
                        self.servo_position[5] += self.step
                    if self.servo_position[4] - self.step in range(1, 999):
                        self.servo_position[4] -= (self.step + 20)
                    if self.servo_position[3] + self.step in range(400, 970):
                        self.servo_position[3] += (self.step + 40)
                    print('Down')
                
                if Char == ord('d'):
                    if self.servo_position[6] + self.step in range(10, 980):
                        self.servo_position[6] -= self.step
                    print('rotate right')
                
                self.keypress_status = True
                
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
                
    

if __name__ == "__main__":
    robot = piarm.PiArm()
    # write your serial comm
    robot.connect("/dev/ttyAMA0")
    keyboard = keyboard()
    #  Start Joystick
    try:
        keyboard.listen()
    #  Set Motors to Default at KeyboardInterrupt
    except KeyboardInterrupt:
        pass
        for ID in range(1, 7):
            robot.servoWrite(ID, 500, 1500)
        