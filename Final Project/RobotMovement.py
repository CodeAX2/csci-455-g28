
from servoCTL import *
from servoCTL import TangoBot

import time
import math

class RobotMovement():
    def __init__(self, robot):
        self.robot = robot

    def turn(self, angle):
        self.robot.setRightTurnSpeed(math.copysign(0.7, angle))
        duration = getTimeToTurnAngle(angle)
        time.sleep(duration/1000)
        self.robot.safeStopMoving()
    
    def move(self, distance):
        speed = 1
        speed = math.copysign(speed, distance)
        self.robot.setSpeed(speed)
        self.robot.setRightTurnSpeed(0)
        duration,finish = getTimeToTravelFeet(1,abs(distance))
        print("Time to travel %d ft. at speed %d is %dms" % (distance,speed,duration))
        time.sleep(duration/1000)
        self.robot.safeStopMoving()
        time.sleep(finish/1000)
    
    def attack(self):
        self.robot.setValue(SERVO_L_ARM_PTICH,-1)
        self.robot.setValue(SERVO_L_ELBOW_PITCH,1)
        self.robot.setValue(SERVO_L_ARM_YAW,-1)
        self.robot.setValue(SERVO_TORSO,0.8)
        time.sleep(0.8)
        self.robot.setValue(SERVO_L_ELBOW_PITCH,0)
        time.sleep(0)
        self.robot.setValue(SERVO_L_ARM_YAW,0)
        self.robot.setValue(SERVO_L_ARM_PTICH,1)
        self.robot.setValue(SERVO_TORSO,-0.8)
        time.sleep(1.0)
        self.robot.setValue(SERVO_L_ARM_PTICH,1)
        self.robot.setValue(SERVO_L_ELBOW_PITCH,0)
        self.robot.setValue(SERVO_TORSO,0)
        self.robot.setValue(SERVO_L_ARM_YAW,0)