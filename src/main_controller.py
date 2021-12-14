#! /usr/bin/python2

import time
import sys
import RPi.GPIO as GPIO
from loadcell_module import LoadCellModule
from relay_module import RelayModule
from rfid_module import RfidModule
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Process

GPIO.setwarnings(False)

# Start the scheduler
sched = BackgroundScheduler()
sched.start()

# # Module interfaces
loadcells = LoadCellModule(dout=21, pd_sck=20)
relays = RelayModule(pd_motor=17, pd_pump=27, pd_circulator=22)
rfid = RfidModule()

def hello_world():
    print("Hello world from main!")
    time.sleep(10)
    print("Bye world from main!")

def cleanAndExit():
    print("Cleaning...")

    GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

# Cancels all jobs given an job array
def cancel_jobs(jobs):
    for job in jobs:
        job.remove()

# ======================================================================
# ===== CONTROLE DE RACAO ==============================================
# ======================================================================
def replanish_ration(size_grams):
    ration_read = loadcells.get_weight_A(11)
    while size_grams > ration_read:
        relays.activate_motor(_time=5)
        ration_read = loadcells.get_weight_A(11)
        time.sleep(0.1)
    print(f'Ration replanished, to a total final {ration_read} grams.')

''' job_list = [{'cron': '', 'size_grams': 150}] '''
def schedule_meals(job_list): 
    jobs = []
    for job in job_list:
        jobs.append(sched.add_job(lambda: replanish_ration(size_grams=job['size_grams']), 'interval', seconds=5))
    return jobs

# job = sched.add_job(lambda: replanish_ration(size_grams=150), 'interval', seconds=5)

# ======================================================================
# ===== MONITORAMENTO RFID =============================================
# ======================================================================
def turn_on_circulator(_time=30):
    print(f'Gato se aproximou, ativando circulador por {_time} segundos.')
    relays.activate_circulator(_time=_time)

# ======================================================================
# ===== REABASTECE AGUA ================================================
# ======================================================================
def replanish_water(water_weight=250):
    water_read = loadcells.get_weight_B(11)
    while water_weight > water_read:
        relays.activate_pump(_time=5)
        water_read = loadcells.get_weight_B(11)
        print(f'water_read {water_read}')
        time.sleep(0.1)

# RECEBE COMUNICACAO COM DO SERVIDOR, deve ser capaz de se comunicar com o servidor,
# realizar registro de tag de rfid e receber novas configuracoes de 

state = {
    'pet_close': False,
    'pet': {
        'name': '',
        'type': ''
    }
}

pw = Process() # water pump
pc = Process() # circulator pump
pr = Process() # ration process
while True:
    try:
        # MONITORA RFID, com o dado da leitura pode-se determinar que pet esta proximo 
        # ativando o circulador caso seja um gato, tambem e possivel determinar qual o
        # pet que esta se alimentando no momento, a partir de monitoramento da racao por
        # medidas na balanca.
        text_read = rfid.read() # Read rfid
        print(text_read)
        if text_read:
            text_read = text_read.strip()
            state['pet_close'] = True
            state['pet']['name'] = text_read.split('.')[0]
            state['pet']['type'] = text_read.split('.')[1]
            print(f'Pet se aproximou, {state["pet"]["name"]}, {state["pet"]["type"]}')
            if state['pet']['type'] == 'gato':
                if pc.is_alive():
                    pc.terminate()
                pc = Process(target=lambda: turn_on_circulator(10))
                pc.start()
                    

        # # MONITORA VASILHA DE AGUA, deve monitorar a vasilha de agua a fim de manter uma
        # # quantidade de agua rasoavel no pote a todo momento.
        # water_read = loadcells.get_weight_B(11)
        # if water_read < 0:
        #     if not pw.is_alive():
        #         pw = Process(target=lambda: replanish_water(50))
        #         pw.start()

        # # ENVIA COMUNICACAO AO SERVIDOR, deve ser capaz de se comunicar com o servidor,
        # # realizar registro de tag de rfid e eventualmente enviar alertas e dados de monitoramento
        
        print('on main')

        if not pr.is_alive():
            pr = Process(target=lambda: replanish_ration(50))
            pr.start()

        time.sleep(1)

    except (Exception, KeyboardInterrupt) as e:
        print(f'Ending: {e}')
        cleanAndExit()
