# -*- coding: utf-8 -*-

import picamera

camera = picamera.PiCamera()
camera.vflip = True

import humanize
from datetime import datetime, timedelta


from telegram.ext import Updater, CommandHandler


def figure(bot, update):
    photo_name = 'pics/{}.jpg'.format(datetime.now().isoformat())
    camera.capture(photo_name)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(photo_name, 'rb'))
    # update.message.reply_text('Hello World!')


def start(bot, update):
    update.message.reply_text('Hello World!')


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))



updater = Updater('389009198:AAGA_q_KOxAKa38nNHiuixDPR1f44baxqwM')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('pic', figure))


updater.start_polling()
updater.idle()