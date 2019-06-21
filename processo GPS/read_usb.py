##
#   -*- coding: utf-8 -*-
#	Arquivo: main.py
#	Autor: Paulo Henrique Rosa
#	Data: 09/06/19
#
#   Descrição: Programa para ler e armazenar dados do GPS 
##



import sys
import glob
import serial


with serial.Serial('/dev/ttyUSB1', 9600, timeout=1) as ser:
    x = ser.read()          # read one byte
    s = ser.read(10)        # read up to ten bytes (timeout)
    line = ser.readline()   # read a '\n' terminated line
