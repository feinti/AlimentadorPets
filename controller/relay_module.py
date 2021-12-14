#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys

class RelayModule:

    def __init__(self, pd_motor, pd_pump, pd_circulator, active_interval=3):
        self.pd_motor = pd_motor
        self.pd_pump = pd_pump
        self.pd_circulator = pd_circulator

        # Set the time for which the motor is activated before load cell is evaluated
        self.active_interval = active_interval

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pd_motor, GPIO.OUT)
        GPIO.setup(self.pd_pump, GPIO.OUT)
        GPIO.setup(self.pd_circulator, GPIO.OUT)

        self.reset()

        # Think about whether this is necessary.
        time.sleep(1)

    def reset(self):
        GPIO.output(self.pd_motor, 1)
        GPIO.output(self.pd_pump, 1)
        GPIO.output(self.pd_circulator, 1)

    def activate_motor(self, _time=0):
        GPIO.output(self.pd_motor, 0)
        if _time is not 0:
            time.sleep(_time)
            self.deactivate_motor()

    def deactivate_motor(self):
        GPIO.output(self.pd_motor, 1)

    def activate_pump(self, _time=0):
        GPIO.output(self.pd_pump, 0)
        if _time is not 0:
            time.sleep(_time)
            self.deactivate_pump()
        
    def deactivate_pump(self):
        GPIO.output(self.pd_pump, 1)

    def activate_circulator(self, _time=0):
        GPIO.output(self.pd_circulator, 0)
        if _time is not 0:
            time.sleep(_time)
            self.deactivate_circulator()

    def deactivate_circulator(self):
        GPIO.output(self.pd_circulator, 1)