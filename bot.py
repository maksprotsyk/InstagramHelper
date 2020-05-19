"""
Telegram bot for instagram recommendations
(main module of the project
"""
import pickle
import random
import telebot
import pandas as pd
from modules.instagram.user_interaction import analyze, get_first_post


BOT = telebot.TeleBot('your api key')

with open('data/model.pickle', 'rb') as in_file:
    MODEL = pickle.load(in_file)

with open('data/stopwords.txt') as in_file:
    STOP_WORDS = in_file.read().split('\n')

DATA_FRAME = pd.read_csv('data/phase7.csv')


@BOT.message_handler(commands=['start'])
def start(message) -> None:
    """
    Allows bot to react to the start command
    """
    BOT.send_message(message.chat.id, 'Привіт!')
    BOT.send_message(message.chat.id,
                     'Я бот, що рекомендує профілі в instagram.')
    BOT.send_message(message.chat.id,
                     'Введи декілька профілів,'
                     ' що тобі подобаються через пробіл.')
    BOT.send_message(message.chat.id, '(Я автоматично відберу'
                                      ' для аналізу'
                                      ' існуючі акаунти, що містять'
                                      ' хоча б 1000 підписників'
                                      ' і менше за 1000 підписок)')


@BOT.message_handler(content_types=['text'])
def process_input(message) -> None:
    """
    Allows bot to react ot user messages
    """
    users = message.text.split()
    recommended = analyze(users, MODEL, DATA_FRAME,
                          stop_words=STOP_WORDS)
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
            if get_first_post(profile):
                BOT.send_message(message.chat.id,
                                 f'<a href="'
                                 f'{get_first_post(profile)}'
                                 f'">Перший пост</a>',
                                 parse_mode='HTML')
            else:
                BOT.send_message(message.chat.id,
                                 'На жаль, не можу отримати'
                                 ' перший пост даного профілю,'
                                 ' спробуйте пізніше')
        BOT.send_message(message.chat.id,
                         'Введіть ще профілі'
                         ' для рекомендації')


if __name__ == '__main__':
    BOT.polling()
