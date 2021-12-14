#! /usr/bin/python2

import time
import sys
import RPi.GPIO as GPIO
from loadcell_module import LoadCellModule
from relay_module import RelayModule
from rfid_module import RfidModule
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Process, Value
import socket
import json
import requests

GPIO.setwarnings(False)

# Envs
SERVER_HOST = '192.168.0.15' # Server IP or Hostname
SERVER_PORT = '3000'
HOST = '192.168.0.241' # Server IP or Hostname
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
JOBS_PORT = 12346 # Pick an open Port (1000+ recommended), must match the client sport
USER_ID = 'tiago_teste'


# Module interfaces
loadcells = LoadCellModule(dout=21, pd_sck=20) # offsetA=202746.63333333333, offsetB=121231.61111111111)
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
    print('Cleaned jobs.')

# ======================================================================
# ===== CONTROLE DE RACAO ==============================================
# ======================================================================
def replanish_ration(size_grams, run_water_pump):
    if run_water_pump.value:
        print('suspending water pump')
        run_water_pump.value = 0
        time.sleep(5)
    
    ration_read = loadcells.get_weight_A(11)
    count = 0
    while size_grams > ration_read:
        relays.activate_motor(_time=2.5)
        ration_read = loadcells.get_weight_A(11)
        time.sleep(0.1)
        count = count + 1
    print('resuming water pump')
    run_water_pump.value = 1
    print(f'Ration replanished, to a total final {ration_read} grams.')

''' job_list = [{'hora': 1, 'minuto': 2, 'size_grams': 150}] '''
def schedule_meals(sched, job_list, run_water_pump):
    jobs = []
    for job in job_list:
        size_grams = job['meal_size_grams']
        hour = job['hora']
        minute = job['minuto']
        jobs.append(sched.add_job(lambda: replanish_ration(size_grams, run_water_pump), 'cron', hour=hour, minute=minute))
        print(f'Scheduled {hour}h {minute}m {size_grams}g')
    print('Scheduled jobs.')
    return jobs

# ======================================================================
# ===== MONITORAMENTO RFID =============================================
# ======================================================================
def turn_on_circulator(_time=30):
    print(f'Gato se aproximou, ativando circulador por {_time} segundos.')
    relays.activate_circulator(_time=_time)

def proximity_read():
    pc = Process() # circulator pump
    while True:
        time.sleep(5)
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
                pc = Process(target=lambda: turn_on_circulator(30))
                pc.start()

# ======================================================================
# ===== REABASTECE AGUA ================================================
# ======================================================================
def replanish_water(run_water_pump, water_weight=-10):
    while True:
        if run_water_pump:
            time.sleep(1)
            water_read = loadcells.get_weight_B(11)
            if water_read < water_weight:
                while 0 > water_read:
                    relays.activate_pump(_time=1)
                    water_read = loadcells.get_weight_B(11)
                    print(f'water_read {water_read}')
                    time.sleep(0.1)
                print(f'final water_read {water_read}')
        else:
            time.sleep(1)

# ======================================================================
# ===== SOCKET CONTROLLER ==============================================
# ======================================================================
def listen_jobs(run_water_pump):
    sched = BackgroundScheduler(timezone='America/Sao_Paulo')
    sched.start()
    meal_jobs = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, JOBS_PORT))
            s.listen()
            print('jobs listening on port: '+ str(JOBS_PORT))
            while True:
                print(meal_jobs)
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        # Logica de tratamento da mensagem vem aqui
                        payload = json.loads(data.decode().split('\n')[-1])
                        print(f'Socket received {payload}')
                        action = payload['action_requested']
                        user_id = payload['user_id']
                        print(f'Action requested: {action}')
                        # ===== fetch_meals ===================================================
                        if action == 'fetch_meals':
                            meals = payload['meals']
                            print(meals)
                            cancel_jobs(meal_jobs)
                            meal_jobs = schedule_meals(sched, meals, run_water_pump)
                            res = {
                                'success': True
                            }
                        # =====================================================================
                        else:
                            res = {
                                'error': f'Action requested to job port <{action}> is not valid.'
                            }
                        body=json.dumps(res)
                        response = f'HTTP/1.1\r\nContent-Type: application/json\r\nAccept: */*\r\nHost: 192.168.0.241:12345\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: {len(body)}\r\n\r\n{body}'

                        conn.sendall(bytes('HTTP/1.1 200 OK', 'utf8'))
                        conn.sendall(bytes(response, 'utf8'))
                        # conn.sendall(bytes(data, 'utf8'))
        except Exception as e:
            print(f'Error while listening on job port {JOBS_PORT}: {e}')

def listen_server(run_water_pump):
    meal_manual_trigger = Process()
    proximity_p = Process()
    timer = Process()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            s.listen()
            print('listening on port: '+ str(PORT))
            while True:
                # == Only one process needs to control rfid ==
                if not proximity_p.is_alive():
                    proximity_p = Process(target=lambda: proximity_read())
                    proximity_p.start()
                # =============================================
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        # Logica de tratamento da mensagem vem aqui
                        payload = json.loads(data.decode().split('\n')[-1])
                        print(f'Socket received {payload}')
                        action = payload['action_requested']
                        user_id = payload['user_id']
                        print(f'Action requested: {action}')
                        # ===== rfid_write ======================================================
                        if action == 'rfid_write':
                            text = payload['text']

                            if proximity_p.is_alive():
                                print('killing prox_p process')
                                proximity_p.terminate()

                            id, text_in = rfid.write(text)
                            if not id:
                                res = {
                                    'error': f'Error writing.'
                                }
                            else:
                                r = requests.post(f'http://{SERVER_HOST}:{SERVER_PORT}/rfid/registerPet', data = {
                                    "tag_id": id,
                                    "user_id": user_id,
                                    "pet_type": text_in.split('.')[1],
                                    "pet_name": text_in.split('.')[0]
                                })
                                res = {
                                    'success': True
                                }
                        # ===== meal_manual_trigger =============================================
                        elif action == 'meal_manual_trigger':
                            meal_size = payload['meal_size_grams']
                            if meal_manual_trigger.is_alive():
                                meal_manual_trigger.terminate()
                            meal_manual_trigger = Process(target=lambda: replanish_ration(meal_size, run_water_pump))
                            meal_manual_trigger.start()
                            res = {
                                'success': True
                            }
                        # =====================================================================
                        else:
                            res = {
                                'error': f'Action requested <{action}> is not valid.'
                            }
                        body=json.dumps(res)
                        response = f'HTTP/1.1\r\nContent-Type: application/json\r\nAccept: */*\r\nHost: 192.168.0.241:12345\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: {len(body)}\r\n\r\n{body}'

                        conn.sendall(bytes('HTTP/1.1 200 OK', 'utf8'))
                        conn.sendall(bytes(response, 'utf8'))
                        # conn.sendall(bytes(data, 'utf8'))
        except Exception as e:
            print(f'Error while listening on port {PORT}: {e}')

# ======================================================================
# ===== ROTINAS DE STARTUP =============================================
# ======================================================================
def startupFetchData():
    r_meals = requests.get(f'http://{SERVER_HOST}:{SERVER_PORT}/meals/fetchMeals', data = {
        "user_id": USER_ID
    })
    if (r_meals.status_code) != 200:
        raise Exception(f'Some error occurred while trying to fetch startup data.\nRequest returned: {r_meals.text}')
    meals = json.loads(r_meals.text)
    print(meals)

state = {
    'pet_close': False,
    'pet': {
        'name': '',
        'type': ''
    }
}
startup = True
pw = Process() # water pump
pr = Process() # ration process
proximity_p = Process() # rfid monitoring process
listen_socket_p = Process() # server process
jobs_socket_p = Process() # jobs process

run_water_pump = Value("i", 1) # evita corrida pela balanca

while True:
    try:
        # # Start to listen to socket
        if not listen_socket_p.is_alive():
            listen_socket_p = Process(target=lambda: listen_server(run_water_pump))
            listen_socket_p.start()
        # Start to listen to socket
        if not jobs_socket_p.is_alive():
            jobs_socket_p = Process(target=lambda: listen_jobs(run_water_pump))
            jobs_socket_p.start()
        # Chama rotinas de startup
        if startup:
            time.sleep(5)
            startupFetchData()
            startup = False

        # MONITORA RFID, com o dado da leitura pode-se determinar que pet esta proximo 
        # ativando o circulador caso seja um gato, tambem e possivel determinar qual o
        # pet que esta se alimentando no momento, a partir de monitoramento da racao por
        # medidas na balanca.
        # ===== foi migrado para o processo que cuida do socket do server =====
                    

        # MONITORA VASILHA DE AGUA, deve monitorar a vasilha de agua a fim de manter uma
        # quantidade de agua rasoavel no pote a todo momento.
        if not pw.is_alive():
                pw = Process(target=lambda: replanish_water(run_water_pump))
                pw.start()


        # # ENVIA COMUNICACAO AO SERVIDOR, deve ser capaz de se comunicar com o servidor,
        # # eventualmente enviar alertas e dados de monitoramento
        
        # print('on main')

        time.sleep(1)

    except (Exception, KeyboardInterrupt) as e:
        print(f'Ending: {e}')
        cleanAndExit()
