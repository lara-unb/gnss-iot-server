import time
import pynmea2
import serial
import pandas as pd

file_path = '../../DATA/EXP1/IOT/logfile.txt'

def read2df(filename):
    df = pd.DataFrame()
    f = open(filename)
    reader = pynmea2.NMEAStreamReader(f)
    
    i=0
    while i<30:
        for msg in reader.next():
            msg_type = msg.sentence_type
            if msg_type == 'GGA':
                print('gga')
            elif msg_type == 'GLL':
                print('gll')
            elif msg_type == 'GSA':
                print('gsa')
            elif msg_type == 'GSV':
                print('gsv')
            elif msg_type == 'RMC':
                print('rmc')
            elif msg_type == 'VTG':
                print('vtg')
            elif msg_type == 'ZDA':
                print('zda')
            elif msg_type == 'TXT':
                print('txt')
            else:
                print(msg_type)
                
        i += 1
        
    f.close()
    return df


def read_serial(filename):
    com = None
    reader = pynmea2.NMEAStreamReader()

    while 1:

        if com is None:
          try:
            com = serial.Serial(filename, timeout=5.0)
          except serial.SerialException:
            print('could not connect to %s' % filename)
            time.sleep(5.0)
            continue

        data = com.read(16)
        for msg in reader.next(data):
          print(msg)

df = read2df(file_path)
