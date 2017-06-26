import kivy

# kivy.require('1.2.0')

import time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.config import Config

Config.set('modules', 'touchring', '')

Weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def getDayOfWeek(dateString):
    t1 = time.strptime(dateString, "%m/%d/%Y")
    t2 = time.mktime(t1)
    return (time.localtime(t2)[6])


class ClockWidget(Scatter):
    uxTime = StringProperty('')
    uxSeconds = NumericProperty(0)
    uxSecondsStr = StringProperty('')
    uxDate = StringProperty('')
    uxDay = StringProperty('')


def update(self, dt):
    self.uxTime = time.strftime("%H:%M", time.localtime())
    self.uxSecondsStr = time.strftime("%S", time.localtime())
    self.uxSeconds = int(self.uxSecondsStr)
    self.uxDate = time.strftime("%d %B %Y", time.localtime())
    self.uxDay = Weekday[getDayOfWeek(time.strftime("%m/%d/%Y", time.localtime()))]


class ClockWidgetApp(App):
    def build(self):
        clockWidget = ClockWidget()
        Clock.schedule_interval(clockWidget.update, 1)
        return clockWidget


if __name__ == '__main__':
    ClockWidgetApp().run()