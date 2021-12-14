#! /usr/bin/python2

import time
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class RfidModule:

    def __init__(self):
        self.reader = SimpleMFRC522()

        # Think about whether this is necessary.
        time.sleep(1)

    def read(self):
        id, text = self.reader.read_no_block()
        if id is None: return ''
        # print(id)
        # print(text)
        return text

    def write(self, text=''):
        try:
            id, text_in = self.reader.write(text)
            print(text)
            return id, text_in
        except Exception as e:
            print(f'Error on write rfid: {e}')
            return None, None
