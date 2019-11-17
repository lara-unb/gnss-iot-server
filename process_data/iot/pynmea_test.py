import time
import datetime
import pynmea2
import serial
import pandas as pd

file_path = '../../DATA/EXP1/IOT/logfile.txt'

def read2df(filename):
    iot_data = {'time':[], 'latitude':[], 'latitude direction':[], 'longitude':[], 'longitude direction':[], 'quality':[], 'in use':[],'PRN in use':[], 'antenna alt':[], #GGA
            # GLL
            'PDOP':[], 'HDOP':[], 'VDOP':[], #GSA
            #RMC
            'speed kmh':[], #VTG
            'date':[] #ZDA
            }

    sat_data = { 'time':[], #GGA
            'PRN':[], #GSA
            'elevation':[], 'azimuth':[], 'SNR':[] # GSV
            }
    
    iot_df = pd.DataFrame(iot_data)
    sat_df = pd.DataFrame(sat_data)
    
    iot_df['latitude direction'] = iot_df['latitude direction'].astype('str')
    iot_df['longitude direction'] = iot_df['longitude direction'].astype('str')
    iot_df['date'] = iot_df['date'].astype('str')
    iot_df['PRN in use'] = iot_df['PRN in use'].astype(object)
    

    f = open(filename)
    reader = pynmea2.NMEAStreamReader(f)

    #time - update on the go
    i=0
    while i<100:
        for msg in reader.next():

            msg_type = msg.sentence_type
            
            if msg_type == 'GGA':
                time = msg.timestamp
                if time not in iot_df['time'].values:
                    iot_df = iot_df.append({'time':time}, ignore_index=True)
                iot_time_idx = iot_df[iot_df['time'] == time].index.values.astype(int)[0]
                       
                iot_df.at[iot_time_idx, 'latitude']=msg.lat
                iot_df.at[iot_time_idx, 'latitude direction']=msg.lat_dir
                iot_df.at[iot_time_idx, 'longitude']=msg.lon
                iot_df.at[iot_time_idx, 'longitude direction']=msg.lon_dir
                iot_df.at[iot_time_idx, 'quality']=msg.gps_qual
                iot_df.at[iot_time_idx, 'in use']=msg.num_sats
                iot_df.at[iot_time_idx, 'antenna alt']=msg.altitude
                
            
            elif msg_type == 'GLL':
                pass
                #print('gll')
            elif msg_type == 'GSA':
                iot_df.at[iot_time_idx, 'PDOP']=msg.pdop
                iot_df.at[iot_time_idx, 'HDOP']=msg.hdop
                iot_df.at[iot_time_idx, 'VDOP']=msg.vdop
                
                sat_list = []
                
                if(msg.sv_id01):
                    sat_list.append(msg.sv_id01)
                if(msg.sv_id02):
                    sat_list.append(msg.sv_id02)
                if(msg.sv_id03):
                    sat_list.append(msg.sv_id03)
                if(msg.sv_id04):
                    sat_list.append(msg.sv_id04)
                if(msg.sv_id05):
                    sat_list.append(msg.sv_id05)
                if(msg.sv_id06):
                    sat_list.append(msg.sv_id06)
                if(msg.sv_id07):
                    sat_list.append(msg.sv_id07)
                if(msg.sv_id08):
                    sat_list.append(msg.sv_id08)
                if(msg.sv_id09):
                    sat_list.append(msg.sv_id09)
                if(msg.sv_id10):
                    sat_list.append(msg.sv_id10)
                if(msg.sv_id11):
                    sat_list.append(msg.sv_id11)
                if(msg.sv_id12):
                    sat_list.append(msg.sv_id12)
                    
                iot_df.at[iot_time_idx, 'PRN in use'] = sat_list
                print(iot_df.at[iot_time_idx, 'PRN in use'])


                #sat_time_idx = iot_df[iot_df['time'] == time].index.values.astype(int)[0]
                
                #sat_df.at[sat_time_idx, 'PRN']=msg.altitude
                    
                #print('gsa')
            elif msg_type == 'GSV':
                
                if msg.sv_prn_num_1:
                    sat_df = sat_df.append({'time':time, 'PRN': msg.sv_prn_num_1, 'elevation':msg.elevation_deg_1, 'azimuth':msg.azimuth_1, 'SNR':msg.snr_1}, ignore_index=True)
                if msg.sv_prn_num_2:
                    sat_df = sat_df.append({'time':time, 'PRN': msg.sv_prn_num_2, 'elevation':msg.elevation_deg_2, 'azimuth':msg.azimuth_2, 'SNR':msg.snr_2}, ignore_index=True)
                if msg.sv_prn_num_3:
                    sat_df = sat_df.append({'time':time, 'PRN': msg.sv_prn_num_3, 'elevation':msg.elevation_deg_3, 'azimuth':msg.azimuth_3, 'SNR':msg.snr_3}, ignore_index=True)
                if msg.sv_prn_num_4:
                    sat_df = sat_df.append({'time':time, 'PRN': msg.sv_prn_num_4, 'elevation':msg.elevation_deg_4, 'azimuth':msg.azimuth_4, 'SNR':msg.snr_4}, ignore_index=True)
                    
                pass
                #print('gsv')
            elif msg_type == 'RMC':
                pass
                #print('rmc')
            elif msg_type == 'VTG':
                iot_df.at[iot_time_idx, 'speed kmh']=msg.spd_over_grnd_kmph
                #print('vtg')
            elif msg_type == 'ZDA':
                time = msg.timestamp
                if time not in iot_df['time'].values:
                    iot_df = iot_df.append({'time':time}, ignore_index=True)
                iot_time_idx = iot_df[iot_df['time'] == time].index.values.astype(int)[0]
                
                iot_df.at[iot_time_idx, 'date']=str(msg.day)+'/'+str(msg.month)+'/'+str(msg.year)
                #print('zda')
            elif msg_type == 'TXT':
                pass
                #print('txt')
            else:
                pass
                #print(msg_type)

        i += 1

    f.close()
    
    iot_df = iot_df.set_index('time')
    sat_df = sat_df.set_index('time','PRN')
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
#print(sat_df)
