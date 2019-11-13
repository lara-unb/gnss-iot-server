import time
import pynmea2
import serial
import pandas as pd

file_path = '../../DATA/EXP1/IOT/logfile.txt'

def read2df(filename):
    iot_data = {'time':[], 'latitude':[], 'latitude direction':[], 'longitude':[], 'longitude direction ':[], 'quality':[], 'in use':[], 'antenna alt':[], #GGA
            # GLL
            'DOP':[], 'HDOP':[], 'VDOP':[], #GSA
            #RMC
            'speed kmh':[], #VTG
            'date':[] #ZDA
            
            }
    
    sat_data = { 'time':[], #GGA
            'PRN':[], #GSA
            'elevation':[], 'azimuth':[], 'SRN':[] # GSV
            }
    
    iot_df = pd.DataFrame(iot_data)
    sat_df = pd.DataFrame(sat_data)
    
    
    f = open(filename)
    reader = pynmea2.NMEAStreamReader(f)
    
    time = 0 #update on the go
    i=0
    while i<30:
        for msg in reader.next():
            msg_type = msg.sentence_type
            if msg_type == 'GGA':
                pass
                #print('gga')
            elif msg_type == 'GLL':
                pass
                #print('gll')
            elif msg_type == 'GSA':
                pass
                #print('gsa')
            elif msg_type == 'GSV':
                pass
                #print('gsv')
            elif msg_type == 'RMC':
                pass
                #print('rmc')
            elif msg_type == 'VTG':
                pass
                #print('vtg')
            elif msg_type == 'ZDA':
                pass
                #print('zda')
            elif msg_type == 'TXT':
                pass
                #print('txt')
            else:
                pass
                #print(msg_type)
                
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
