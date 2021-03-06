#! /usr/bin/python2

import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

referenceUnitA = 1117
referenceUnitB = 276

class LoadCellModule:

    def __init__(self, dout, pd_sck, offsetA=None, offsetB=None):
        self.PD_SCK = pd_sck
        self.DOUT = dout

        self.hx = HX711(dout=dout, pd_sck=pd_sck)
        self.hx.set_reading_format("MSB", "MSB")

        self.hx.set_reference_unit_A(referenceUnitA)
        self.hx.set_reference_unit_B(referenceUnitB)

        if offsetA is not None:
            self.hx.reset()
            self.hx.set_offset_A(offsetA)
        else:
            self.reset_and_tare_A()
        if offsetB is not None:
            self.hx.reset()
            self.hx.set_offset_B(offsetB)
        else:
            self.reset_and_tare_B()

        # Think about whether this is necessary.
        time.sleep(1)

    def reset_and_tare_A(self):
        self.hx.reset()
        self.hx.tare_A()
        print("Tare A done!")

    def reset_and_tare_B(self):
        self.hx.reset()
        self.hx.tare_B()
        print("Tare B done!")

    def get_weight_A(self, num_reads=25):
        return max(0, round(self.hx.get_weight_A(num_reads)))

    def get_weight_B(self, num_reads=25):
        return round(self.hx.get_weight_B(num_reads))

