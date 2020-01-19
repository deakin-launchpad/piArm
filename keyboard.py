import re
import pygame
import piarm
from time import sleep

class Keyboard(object):

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
        
        pygame.init()
        
        

        #  Initialize Keyboard
        
        print('Keyboard initialized')
        
        self.read_servo_position()
        print(self.servo_position)
        
    
    def listen(self):
        
        # Initialize Display
        
        win = pygame.display.set_mode((500,500))
        pygame.display.set_caption("PiArm")
        
        #Initialize keyboard instruction
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or pygame.KEYUP:
                    if event.type == pygame.QUIT:
                        run = False           
                
                
                    keys = pygame.key.get_pressed()
                    
                    #Default position
                    if keys[pygame.K_q] == True:
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
                    
                    #rotate left
                    if keys[pygame.K_LEFT] or keys[pygame.K_a] == True:
                        
                        if self.servo_position[6] - self.step in range(10, 980):
                            self.servo_position[6] += self.step
                        
                        print('left')
                        
                    #rotate right
                    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] == True:
                        
                        if self.servo_position[6] + self.step in range(10, 980):
                            self.servo_position[6] -= self.step
                       
                        print('right')
                        
                    #Move servo 3,4,5 UP
                    elif keys[pygame.K_UP] or keys[pygame.K_w]== True:
                        if self.servo_position[5] + self.step in range(101, 999):
                            self.servo_position[5] += self.step
                        if self.servo_position[4] - self.step in range(1, 999):
                            self.servo_position[4] -= (self.step + 20)
                        if self.servo_position[3] + self.step in range(400, 970):
                            self.servo_position[3] += (self.step + 40)
                        
                        print('up')
                        
                    #Move servo 3,4,5 down
                    elif keys[pygame.K_DOWN] or keys[pygame.K_s]== True:
                        
                        if self.servo_position[5] - self.step in range(101, 999):
                            self.servo_position[5] -= self.step
                        if self.servo_position[4] + self.step in range(1, 999):
                            self.servo_position[4] += (self.step + 20)
                        if self.servo_position[3] - self.step in range(400, 970):
                            self.servo_position[3] -= (self.step + 40)
                        print('down')
                        
                    #claw close
                    elif keys[pygame.K_SPACE] == True:
                        if self.servo_position[1] + self.step in range(144, 710):
                            self.servo_position[1] += (self.step + 20)
                            
                        print('close')
                        
                    #claw open
                    elif keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL] == True:
                        if self.servo_position[1] - self.step in range(144, 710):
                            self.servo_position[1] -= (self.step + 20)
                        print('open')
                    
                    #Move servo 5 backward
                    elif keys[pygame.K_e] == True:
                        if self.servo_position[5] - self.step in range(10, 999):
                            self.servo_position[5] += self.step
                    
                    #Move servo 5 forward
                    elif keys[pygame.K_f] == True:
                        if self.servo_position[5] + self.step in range(10, 999):
                            self.servo_position[5] -= self.step
                                            
                    
                    self.keypress_status = True                    
                    #pygame.display.update()
                    
                    
            #  Write current positions
            if self.keypress_status:
                if robot.alive:
                    for ID in range(1, 7):
                        robot.servoWrite(ID, self.servo_position[ID], 1000)
                        print("Writing to servo Id {} position: ".format(ID), self.servo_position[ID])
                    self.keypress_status = False
                else:
                    print('Comm port is not conected')
                sleep(1)
            
            
    def read_servo_position(self):
        '''
        This funciton read current servo position
        '''
        if robot.alive:
            try:
                #  Read Positions of motors one at a time
                for ID in range(1, 7):
                    response = robot.positionRead(ID)
                    pos = int.from_bytes(response[5]+response[6], byteorder='little')    
                    #  Button Position to variable
                    self.servo_position[ID] = pos
                        
                if self.servo_POS_error:
                    print("Servo Error", "Servo " + str(ID) +
                                     ' - Position Out of Range..!')
                else:
                    print("Motor position Read Done Successfully")
                    
            except TypeError:
                print("Servo Error", "Servo " + str(ID) +
                                     ' - Not Responding')
        

if __name__ == "__main__":
    robot = piarm.PiArm()
    # write your serial comm
    robot.connect("/dev/ttyAMA0")
    keyboard = Keyboard()
    #  Start KEYBOARD
    keyboard.listen()
    
    pygame.quit()
