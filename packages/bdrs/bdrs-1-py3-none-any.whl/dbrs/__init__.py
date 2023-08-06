from threading import Thread
import dbrs.cfg as cfg
from subprocess import PIPE, run

import telebot

import re


def _sendd(chatid, file):
    global bot
    
    with open(file, 'rb') as f:
        bot.send_document(chatid, f)  # Отправка документа


def _send(chatid, text, pm='HTML',):
    global bot
    print(text)
    if len(text) < 4096:
        bot.send_message(chat_id=chatid,
                         parse_mode=pm,
                         text=text)  # Отправка текста
    else:
        ofset = 0
        while ofset < len(text):
            bot.send_message(chat_id=chatid, parse_mode=pm,
                             text=text[ofset:ofset + 4096])
            ofset += 4096


def _run(command):
    result = run(command, stdout=PIPE, shell=True,
                 stderr=PIPE, universal_newlines=True)
    print('> '+command)
    if result.stderr == "":
        print(result.stderr)
        return result.stdout  # Отправка только вывода

    else:
        print(result.stdout + "\nSTDERR:\n" + result.stderr)
        return result.stdout + "\nSTDERR:\n" + result.stderr  # Отправка вывода и ошибки


def start():
    global bot
    
    print('starting...')
    TOKEN = cfg.tgtoken
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(msg):
        print(msg.json)
        if msg.json['from']['id'] == cfg.chat:
            res = _run(msg.json['text'])
            try:
                _send(cfg.chat, res)
            except telebot.apihelper.ApiTelegramException:
                with open(".cmd.out", 'w') as f:
                    f.truncate(0)
                    f.write(res)
                _sendd(cfg.chat, ".cmd.out")

    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    print('exiting...')

Thread(target=start).start()
