#! /usr/bin/python2

import time
import sys
import pandas as pd
from os.path import exists

queue_state = [0, 0, 0]

class LocalStorageController:

    def __init__(self, relative_storage_path='./storage'):
        self.storage_path = relative_storage_path
        if not exists(self.storage_path+'/lock.csv')
            df = pd.DataFrame(data=[], index=('main', 'socket', 'server'))
            df.to_csv(self.storage_path+'/lock.csv')

    def grab_lock(self, index, priority=0):
        if priority is 0:
            
        self.hx.reset()
        self.hx.tare_A()
        print("Tare A done!")
