# -*- coding: utf-8 -*-

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def get_data_from_mc():
    data = ["CO2", "T", "ts"]
    value = mc.get_multi(data)
    return "{}\nCO2: {}ppm\nT: {}°C".format(value['ts'],
                                            value['CO2'],
                                            value['T'],
                                            )

from telegram.ext import Updater, CommandHandler

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


updater.start_polling()
updater.idle()