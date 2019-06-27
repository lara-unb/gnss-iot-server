##
#   -*- coding: utf-8 -*-
#	Arquivo: main.py
#	Autor: Paulo Henrique Rosa
#	Data: 09/06/19
#
#   Descrição: Programa para ler e armazenar dados do GPS
##


from serial import Serial
import serial.tools.list_ports


def write_data(data):
    file_name = 'logfile.txt'
    with open(file_name, 'a') as file_object:
        file_object.write(data)


def available_port():

    print('[*] Please, choose a serial port !\n')
    ports = serial.tools.list_ports.comports()

    for port in ports:
        print(port)
    print()
    answer = input("Port: ")
    return answer


def open_port(port):

    try:
        SerialPort = serial.Serial(port)
        SerialPort.baudrate = 9600
        SerialPort.bytesize = 8
        SerialPort.parity = 'N'
        SerialPort.stopbits = 1

    except serial.SerialException:
        print("[*] Unable open serial port !")
        exit(1)

    return SerialPort


if __name__ == "__main__":
    port = available_port()
    SerialPort = open_port(port)
    while True:
        data = SerialPort.readline()
        data = data.decode(encoding='utf-8', errors='strict') 
        print(data)
        write_data(data)
