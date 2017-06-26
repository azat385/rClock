# -*- coding: utf-8 -*-

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

import socket
import time
from struct import unpack

hexString = lambda byteString : " ".join(x.encode('hex') for x in byteString)

TCP_IP = '192.168.155.11'
TCP_PORT = 4001
BUFFER_SIZE = 1024

getPowerCRC = "\x10\x03\x01\x00\x00\x02\xC6\xB6"


def getMB():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(getPowerCRC)
    data = s.recv(BUFFER_SIZE)
    s.close()
    # print "write: {}\nread:  {}".format(hexString(getPowerCRC), hexString(data))
    data = unpack(">BBBHHBB", data)
    # print data[3:5]
    return "{}ppm {}°C".format(data[3]/10.0, data[4]/10.0)


class DataLabel(Label):
    def update(self, *args):
        self.text = getMB()


class IncrediblyCrudeClock(Label):
    def update(self, *args):
        self.text = time.asctime()

class TimeApp(App):
    def build(self):
        crudeclock = IncrediblyCrudeClock()
        d = DataLabel()
        Clock.schedule_interval(d.update, 5)
        Clock.schedule_interval(crudeclock.update, 1)
        # root = GridLayout(cols=2, padding=50, spacing=50)
        root = BoxLayout(orientation='vertical')
        root.add_widget(crudeclock)
        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(d)
        root.add_widget(layout)
        return root

if __name__ == "__main__":
    TimeApp().run()