import time
import datetime
import pynmea2
import serial
import pandas as pd

file_path = '../../DATA/EXP1/IOT/logfile.txt'

def read2df(filename):
    iot_data = {'time':[datetime("00:00:00").time()], 'latitude':[0], 'latitude direction':['S'], 'longitude':[0], 'longitude direction ':['W'], 'quality':[0], 'in use':[0], 'antenna alt':[0], #GGA
            # GLL
            'DOP':[0], 'HDOP':[0], 'VDOP':[0], #GSA
            #RMC
            'speed kmh':[0], #VTG
            'date':[datetime("0".date())] #ZDA
            }

    sat_data = { 'time':[], #GGA
            'PRN':[], #GSA
            'elevation':[], 'azimuth':[], 'SRN':[] # GSV
            }
<<<<<<< HEAD
    
    iot_df = pd.DataFrame(iot_data).set_index('time')
    sat_df = pd.DataFrame(sat_data).set_index('time')
    
    
=======

    iot_df = pd.DataFrame(data=iot_data).set_index('time')
    sat_df = pd.DataFrame(data=sat_data).set_index(['time','PRN'])

>>>>>>> 2a1b39d10b383de1eda05bac628cc58ebebcd34a
    f = open(filename)
    reader = pynmea2.NMEAStreamReader(f)

    #time - update on the go
    i=0
    while i<100:
        for msg in reader.next():

            msg_type = msg.sentence_type

            if msg_type == 'GGA':
                time = msg.timestamp
<<<<<<< HEAD
                print(time)
                sat_df = sat_df.append({'time':time}, ignore_index=True)
                #sat_df.ix[time]=
                print(sat_df)
                #print('gga')
=======
                if time not in iot_df.index:

                    print(time)
                    iot_df.append(pd.Series(name=time), ignore_index=False)
                    print(iot_df)

                iot_df[time]['latitude']=msg.lat
                iot_df[time]['latitude direction']=msg.lat_dir
                iot_df[time]['longitude']=msg.lon
                iot_df[time]['longitude direction']=msg.lon_dir
                iot_df[time]['quality']=msg.gps_qual
                iot_df[time]['in use']=msg.num_sats
                iot_df[time]['antenna alt']=msg.altitude
>>>>>>> 2a1b39d10b383de1eda05bac628cc58ebebcd34a
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
<<<<<<< HEAD
=======
print(iot_df)
>>>>>>> 2a1b39d10b383de1eda05bac628cc58ebebcd34a
