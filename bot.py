"""
Telegram bot for instagram recommendations
"""
import pickle
import random
import telebot
import pandas as pd
from modules.Instagram.user_interaction import analyze, get_first_post


BOT = telebot.TeleBot('1196552839:AAGMLq4rKPThtsvR5XmGs3YVOC-rZcfg15Y')

with open('data/model.pickle', 'rb') as in_file:
    MODEL = pickle.load(in_file)

DATAFRAME = pd.read_csv('data/phase7.csv')


@BOT.message_handler(commands=['start'])
def start(message):
    """
    Allows bot to react to the start command
    """
    BOT.send_message(message.chat.id, 'Привіт!')
    BOT.send_message(message.chat.id,
                     'Я бот, що рекомендує профілі в Instagram.')
    BOT.send_message(message.chat.id,
                     'Введи декілька профілів,'
                     ' що тобі подобаються через пробіл.')
    BOT.send_message(message.chat.id, '(Я автоматично відберу'
                                      ' для аналізу'
                                      ' існуючі акаунти, що містять'
                                      ' хоча б 1000 підписників'
                                      ' і менше за 1000 підписок)')


@BOT.message_handler(content_types=['text'])
def process_input(message):
    """
    Allows bot to react ot user messages
    """
    users = message.text.split()
    recommended = analyze(users, MODEL, DATAFRAME)
    if recommended is None:
        BOT.send_message(message.chat.id,
                         'На жаль, дані профілі'
                         ' містять замало інформації')
    else:
        random.shuffle(recommended)
        recommended = recommended[:3]
        for num, profile in enumerate(recommended):
            BOT.send_message(message.chat.id,
                             f'Рекомендація {num+1}:')
            BOT.send_message(message.chat.id,
                             f'<a href="http://www.'
                             f'instagram.com/{profile}">'
                             f'{profile}</a>',
                             parse_mode='HTML')
            BOT.send_message(message.chat.id,
                             f'<a href="{get_first_post(profile)}">'
                             f'Перший пост</a>',
                             parse_mode='HTML')
        BOT.send_message(message.chat.id,
                         'Введіть ще профілі'
                         ' для рекомендації')


if __name__ == '__main__':
    BOT.polling()
