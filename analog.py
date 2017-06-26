# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout
from math import cos, sin, pi
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

import datetime

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
    return "CO2: {}ppm  T: {}°C".format(data[3]/10, data[4]/10.0)


class DataLabel(Label):
    def update(self, *args):
        self.text = getMB()
        self.font_size = 15
        # self.color = (1, 0, 0, 1)

kv = '''
#:import math math

[ClockNumber@Label]:
    text: str(ctx.i)
    pos_hint: {"center_x": 0.5+0.42*math.sin(math.pi/6*(ctx.i-12)), "center_y": 0.5+0.42*math.cos(math.pi/6*(ctx.i-12))}
    font_size: self.height/8

<MyClockWidget>:
    face: face
    ticks: ticks
    FloatLayout:
        id: face
        size_hint: None, None
        pos_hint: {"center_x":0.5, "center_y":0.5}
        size: 0.9*min(root.size), 0.9*min(root.size)
        canvas:
            Color:
                rgb: 0.1, 0.1, 0.1
            Ellipse:
                size: self.size     
                pos: self.pos
        ClockNumber:
            i: 1
        ClockNumber:
            i: 2
        ClockNumber:
            i: 3
        ClockNumber:
            i: 4
        ClockNumber:
            i: 5
        ClockNumber:
            i: 6
        ClockNumber:
            i: 7
        ClockNumber:
            i: 8
        ClockNumber:
            i: 9
        ClockNumber:
            i: 10
        ClockNumber:
            i: 11
        ClockNumber:
            i: 12
    Ticks:
        id: ticks
        r: min(root.size)*0.9/2
'''
Builder.load_string(kv)

class MyClockWidget(FloatLayout):
    pass


k = 1.15

class Ticks(Widget):
    def __init__(self, **kwargs):
        super(Ticks, self).__init__(**kwargs)
        self.bind(pos=self.update_clock)
        self.bind(size=self.update_clock)

    def update_clock(self, *args):
        self.canvas.clear()
        with self.canvas:
            time = datetime.datetime.now()
            Color(1.0, 1.0, 1.0)
            Line(points=[self.center_x, self.center_y*k, self.center_x+0.8*self.r*sin(pi/30*time.second), self.center_y*k+0.8*self.r*cos(pi/30*time.second)], width=2, cap="round")
            Color(1.0, 1.0, 1.0)
            Line(points=[self.center_x, self.center_y*k, self.center_x+0.7*self.r*sin(pi/30*time.minute), self.center_y*k+0.7*self.r*cos(pi/30*time.minute)], width=3, cap="round")
            Color(1.0, 1.0, 1.0)
            th = time.hour*60 + time.minute
            Line(points=[self.center_x, self.center_y*k, self.center_x+0.5*self.r*sin(pi/360*th), self.center_y*k+0.5*self.r*cos(pi/360*th)], width=4, cap="round")

class MyClockApp(App):
    def build(self):
        d = DataLabel()
        Clock.schedule_interval(d.update, 5)
        clock = MyClockWidget()
        Clock.schedule_interval(clock.ticks.update_clock, 1)

        root = BoxLayout(orientation='vertical')
        root.add_widget(clock)
        layout = BoxLayout(size_hint=(1, None), height=d.height)
        layout.add_widget(d)
        root.add_widget(layout)
        return root


if __name__ == '__main__':
    MyClockApp().run()
