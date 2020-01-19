import sys


RANGE_START = 1
RANGE_END = 7


class Arm():
    # left arm = 51 - 56, start_index = 50
    # right arm = 1 - 6, start_index = 0
    def __init__(self, robot, start_index:int):
        self.start_index = start_index
        self.robot = robot
        self.servo_position = {}
        for i in range (RANGE_START, RANGE_END):
            if (i == 5):
                self.servo_position[self.start_index + i] = 200
                continue
            self.servo_position[self.start_index + i] = 500
        self.write_servo()

    def claw_rotate(self, value):
        self.servo_position[self.start_index + 2] = value
        self.write_servo()

    def claw_spread(self, value):
        self.servo_position[self.start_index + 1] = value
        self.write_servo()

    def write_servo(self):
        if self.robot.alive:
            for i in range (RANGE_START, RANGE_END):
                self.robot.servoWrite(i, self.servo_position[self.start_index + i], 1000)
