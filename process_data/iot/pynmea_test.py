import time
import datetime
import pynmea2
import serial
import pandas as pd

file_path = '../../DATA/EXP1/IOT/logfile.txt'

def read2df(filename):
    iot_data = {'time':[], 'latitude':[], 'latitude direction':[], 'longitude':[], 'longitude direction':[], 'quality':[], 'in use':[], 'antenna alt':[], #GGA
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

    #time - update on the go
    i=0
    while i<300:
        for msg in reader.next():

            msg_type = msg.sentence_type

            if msg_type == 'GGA':
                time = msg.timestamp

                
                
                if time not in iot_df['time'].values:
                    iot_df = iot_df.append({'time':time}, ignore_index=True)
                
                
                iot_df['latitude direction'] = iot_df['latitude direction'].astype('str')
                iot_df['longitude direction'] = iot_df['longitude direction'].astype('str')

                time_idx = iot_df[iot_df['time'] == time].index.values.astype(int)[0]
                
                
                print(msg.lon_dir)
                iot_df.at[time_idx, 'latitude']=msg.lat
                iot_df.at[time_idx, 'latitude direction']=msg.lat_dir
                iot_df.at[time_idx, 'longitude']=msg.lon
                iot_df.at[time_idx, 'longitude direction']=msg.lon_dir
                iot_df.at[time_idx, 'quality']=msg.gps_qual
                iot_df.at[time_idx, 'in use']=msg.num_sats
                iot_df.at[time_idx, 'antenna alt']=msg.altitude

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
    
    #iot_df = iot_df.set_index('time')
    #sat_df = sat_df.set_index('time')
    return iot_df, sat_df


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

iot_df, sat_df = read2df(file_path)
#print(iot_df)
