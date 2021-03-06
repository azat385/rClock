# -*- coding: utf-8 -*-
from serial import Serial
from struct import pack, unpack
from time import sleep
from datetime import datetime

from sql_create_table import Data, session, check_if_data_table_exists

hexString = lambda byteString : " ".join(x.encode('hex') for x in byteString)

# ser = Serial(
#     port='COM1',
#     baudrate=9600,
#     bytesize=8,
#     parity='N',
#     stopbits=1,
#     timeout=0.5,
#     xonxoff=0,
#     rtscts=0
# )

# sample rq&rs
getPowerCRC = "\x10\x03\x01\x00\x00\x02\xC6\xB6"
# ser.write(getPowerCRC)
# response = ser.read(size=100)
# print "write: {}\nread:  {}".format(hexString(getPowerCRC),hexString(response))

import socket

# TCP_IP = '192.168.155.11'
# TCP_PORT = 4001
# TCP_IP = '194.87.99.184'
TCP_IP = '127.0.0.1'
TCP_PORT = 14220
BUFFER_SIZE = 1024

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

check_if_data_table_exists()

for _ in range(8):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect((TCP_IP, TCP_PORT))
    s.send(getPowerCRC)
    data = s.recv(BUFFER_SIZE)
    s.close()

    ts = datetime.now()
    print "write: {}\nread:  {}".format(hexString(getPowerCRC),hexString(data))
    data = unpack(">BBBHHBB", data)
    print "{}ppm {}°C".format(data[3]/10, data[4]/10)

    mc.set("CO2", data[3])
    mc.set("T", data[4])
    mc.set("ts", ts)

    session.add(Data(tag_id=1, value=data[3] / 10, stime=ts))
    session.add(Data(tag_id=2, value=data[4] / 10.0, stime=ts))
    session.commit()

    sleep(5)
