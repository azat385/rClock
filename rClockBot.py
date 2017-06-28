# -*- coding: utf-8 -*-

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

import humanize
from datetime import datetime, timedelta


from plotly.offline import plot
from plotly.graph_objs import Bar, Scatter


def get_data_from_mc():
    data = ["CO2", "T", "ts"]
    value = mc.get_multi(data)
    _t = humanize.i18n.activate('ru_RU')
    return "{}({})\nCO2: {}ppm\nT: {}°C".format(humanize.naturaltime(datetime.now() - value['ts']),
                                            value['ts'],
                                            value['CO2']/10,
                                            value['T']/10.0,
                                            )

from telegram.ext import Updater, CommandHandler


def figure(bot, update):
    update.message.reply_text('Hello World!')


def start(bot, update):
    update.message.reply_text('Hello World!')


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def data(bot, update):
    update.message.reply_text(get_data_from_mc())

updater = Updater('394896923:AAFHq9Y3efI_kO44cVNeuRAwBtJTpplBLKs')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('data', data))
updater.dispatcher.add_handler(CommandHandler('pic', figure))


updater.start_polling()
updater.idle()