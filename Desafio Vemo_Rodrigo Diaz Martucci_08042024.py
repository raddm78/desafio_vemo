import random
import time
from time import sleep

signal_dictionary = [
 "Main Battery Voltage",
 "Main Battery Current",
 "Speed",
 "Main Battery Temperature",
 "Door Open",
 "Tire Pressure"
]

alarms_setup = [
 "alarm Main Battery Voltage",
 "alarm Main Battery Current",
 "alarm Speed",
 "alarm Main Battery Temperature",
 "alarm Door Open",
 "alarm Tire Pressure"
]

alarmas_conduccion_peligrosa = [
 "alarm_speed"
]

class Signal:
 def __init__(self, id, val):
  self.id = id
  self.val = val

def get_alarm(signals, alarmas_signals):
 
 for j in range(len(signal_dictionary)):
  id = j+1
  v = 0
  if (id == 1)and(signals[j].val <=360):
   v = 1
  elif (id == 2)and((signals[j].val <=0)or(signals[j].val >40)):
   v = 1
  elif (id == 3)and(signals[j].val >=100):
   v = 1  
  elif (id == 4)and(signals[j].val > 75):
   v = 1
  if (id == 5)and(signals[j].val == 0):   # la alarma se pone en 1 si la puerta esta abierta(0)
   v = 1
  if (id == 6)and((signals[j].val == 28)or(signals[j].val == 34)):
   v = 1
  alarmas_signals[j] = Signal(id, v) 

debug = True # Set to True for debug mode, False for regular mode

def get_data_row(signals):
 
 for i in range(len(signal_dictionary)):
  signal_id = i + 1
  value = 0
  if signal_id == 1:
    value = random.randint(350, 449) 
  elif signal_id == 2:
    value = random.randint(-50, 49)
  elif signal_id == 3:
    value = random.randint(0, 149)  
  elif signal_id == 4:
    value = random.randint(20, 99)
  elif signal_id == 5:
    value = random.randint(0, 1)
  elif signal_id == 6:
    value = random.randint(28, 34)
  signals[i] = Signal(signal_id, value)

def organizar_alarmas(alarms_signals, alarms_signals_cp):   # Funcion para separar las alarmas de conduccion peligrosa y las de problema en el vehiculo.
 for i in range(len(alarms_signals)):
  id = i + 1
  if id == 3:
   for j in range(len(alarms_signals_cp)):
    v = alarms_signals[id].val
    alarms_signals_cp[j] = Signal(id, v) 

def send_data_to_server(signals, timestamp, alarms_signals):
 global debug
 global aux   # aux es una lista auxiliar para guardar los valores de signals   
 if debug:
  print("\nSending data to server...")
  print("Data sent:")
 for i in range(len(signal_dictionary)):
  if debug:
   if aux[i]!=signals[i].val:   # Evalua que el valor anterior (1 seg antes) sea distinto al presente.
    print(f"Signal: {signal_dictionary[i]}, Value: {signals[i].val}, Time: {timestamp}")
    if alarms_signals[i].val != 0:
     if i != 2:   # solo envia las alarmas activadas (en 1)
      print(f"Alarmas de Problemas en el Vehiculo: {alarms_setup[i]}, Value: {alarms_signals[i].val}, Time: {timestamp}")  # Alarmas por falla en el vehiculo
     else:
      print(f"Alarmas de Conduccion Peligrosa: {alarms_setup[i]}, Value: {alarms_signals[i].val}, Time: {timestamp}")  # Alarmas por manejo inapropiado
    aux[i] = signals[i].val   # Le asigno a la lista auxiliar los valores de signals para ser comparados en el proximo periodo de tiempo

  else:   # Modo Debug False, solo envia el timestamp, ID y valores de sensores y alarmas. No repite data al server
    for i in range(len(signal_dictionary)):
     if aux[i]!=signals[i].val:
      print(f"{timestamp},{signals[i].id},{signals[i].val},{alarms_signals[i].val}")
      aux[i] = signals[i].val

def main():
 global debug
 global aux
 data_period = 1 # 1 second
 aux = [None] * len(signal_dictionary)  #comparador para no enviar al server dato repetido en t-1
 while True:
  signals = [None] * len(signal_dictionary)
  alarms_signals = [None] * len(alarms_setup)
  alarms_signals_cp = [None] * len(alarmas_conduccion_peligrosa)
  timestamp = int(time.time())
  get_data_row(signals)
  get_alarm(signals, alarms_signals)
  organizar_alarmas(alarms_signals, alarms_signals_cp)
  send_data_to_server(signals, timestamp, alarms_signals)
  sleep(data_period)

if __name__ == "__main__":
 main()