import telebot
from DataBase import HomeWork as HW, Schedule as sch, Students as st
from TgBotUI import configuration
from TgBotUI import utils
import requests
import pprint
import datetime
import re

bot = telebot.TeleBot(configuration.token)
MAIN_URL = f'https://api.telegram.org/bot{configuration.token}'

global step

@bot.message_handler(commands=['start'])
def start_menu(message):
    message_text = 'Здравствуйте!\n' \
                   + 'Наберите /setgroup Группа Фамилия Имя - для ввода Вашего номера группы и фамилии и имени через пробел'
    bot.send_message(message.chat.id, message_text)
    print(message.chat)


@bot.message_handler(commands=['setgroup'])
def set_group(message):
    # arguments = []
    # print(message.text.split(" ")[1:])
    arguments = message.text.split(" ")[1:]
    print(arguments)
    arguments.insert(2, arguments.pop(0))
    print(arguments)
    print(st.update_tg_login(arguments[0], arguments[1], arguments[2], message.chat.username))
    bot.send_message(message.chat.id,
                     st.update_tg_login(arguments[0], arguments[1], arguments[2], message.chat.username))

@bot.message_handler(commands=['changegroup'])
def set_group(message):
    arguments = message.text.split(" ")[1:]
    #print(arguments)
    bot.send_message(message.chat.id, st.change_group_num(arguments[0], arguments[1], arguments[2], arguments[3]))


@bot.message_handler(commands=['getgroup'])
def get_group(message):
    bot.send_message(message.chat.id, st.get_group_num(message.chat.username)["pgroup"])


@bot.message_handler(commands=['schedule'])
def get_schedule(message):
    group = st.get_group_num(message.chat.username)["pgroup"]
    print(group)
    test = sch.read_schedule(group, "10:00-11:40 20.10.2020")
    print(test)
    bot.send_message(message.chat.id, sch.read_schedule(group, "10:00-11:40 20.10.2020"))








# @bot.message_handler(text=['->'])
# def next_week(message):
#     global step
#     step = step + 1
#     bot.send_message(message.chat.id, reply_markup=utils.generate_keyboards()[step])





@bot.message_handler(commands=['report'])
def set_group(message):
    bot.send_message(message.chat.id, 'Новости и погода на сегодня: ')


# keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
# keyboard1.row('button1', 'button2', 'button3', 'button4')
# keyboard1.row('button5', 'button6', '->')


# def generate_keyboard(week):
#     keyboardDates = telebot.types.InlineKeyboardMarkup()
#     key_day1 = telebot.types.InlineKeyboardMarkup(text = "21.12.2020", callback_data="day1")
#     keyboardDates.add(key_day1)
#     key_next_ = telebot.types.InlineKeyboardMarkup(text = "21.12.2020", callback_data="day1")
#     keyboardDates.add(key_day1)


@bot.message_handler(commands=['tasklist'])
def get_homework(message):
    #print(st.get_group_num(message.chat.username))
    bot.send_message(message.chat.id, 'Задание на неделю:', reply_markup=utils.generate_keyboards()[0])
    #bot.send_message(message.chat.id, 'Задание')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    result = call.data.split("_")
    if result[0] == "tasklist":
        print(result)
        if result[1] == "👉🏿":
            step = int(result[2]) + 1
        elif result[1] == "👈🏿":
            step = int(result[2]) - 1
            print(call.data)
        elif result[3] != result[1]:
            step = int(result[2])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=result[1],
                                  reply_markup=utils.generate_keyboards(additional=f'_{result[1]}')[step])
            return
        else:
            return
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(step),
                              reply_markup=utils.generate_keyboards()[step])



# @bot.message_handler(commands=['test'])
# def test(message):
#     bot.send_message(message.chat.id, 'Тест', reply_markup=utils.generate_keyboards()[0])

@bot.message_handler(commands=['hometask'])
def get_hometask(message):
    # bot.send_message(message.chat.id, 'Введите дату или выберите ее из списка', reply_markup=keyboard1)
    bot.send_message(message.chat.id, 'Выберите дату из списка', reply_markup=utils.generate_keyboards()[0])

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    result = call.data.split("_")
    if result[0] == "hometask":
        print(result)
        if result[1] == "👉🏿":
            step = int(result[2]) + 1
        elif result[1] == "👈🏿":
            step = int(result[2]) - 1
            print(call.data)
        elif result[3] != result[1]:
            step = int(result[2])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=result[1],
                                  reply_markup=utils.generate_keyboards(additional=f'_{result[1]}')[step])
            return
        else:
            return
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(step),
                              reply_markup=utils.generate_keyboards()[step])



# @bot.message_handler(content_types=['text'])
# def next_week(message):
#     global week
#     if message.text == "->":
#         week += 1
#         bot.send_message(message.chat.id, f"Страница с расписанием на {week} неделю: ", reply_markup=keyboard2)
#         print("Handled")


# keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
# keyboard2.row('<-', 'button1', 'button2', 'button3', 'button4')
# keyboard2.row('button5', 'button6', '->')


# @bot.message_handler(text=['->'])
# def next_week(message):
#     bot.send_message(message.chat.id, reply_markup=keyboard2)


# @bot.message_handler(commands=['help'])
# def print_menu(message):
#     message_text = 'Вот, что умеет этот бот:\n' \
#                    + '/help - отображает список доступных команд\n' \
#                    + '/setgroup - Необходимо ввести свой номер группы'
#     bot.send_message(message.chat.id, message_text)

# keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
# keyboard1.row('/show', 'Пока')


# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     if message.text == '3530904/70105 Лысенко Владислав':
#         bot.send_message(message.chat.id, 'Ваш номер группы: 3530904/70105. Вы подписались на ' +
#                                           ' автоматическое уведомление о расписании занятий на следующий день.')
#
#     else:
#         bot.send_message(message.chat.id, 'Такого номера группы не существует')


# keyboard2 = telebot.types.ReplyKeyboardMarkup(True,True)
# keyboard2.row('button1', 'button2', 'button3','button4')
# keyboard2.row('button5', 'button6', 'button7','button8')
# @bot.message_handler(commands=['show'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Привет, ты написал мне /show', reply_markup=keyboard2)


# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     if message.text == '3530904/70102':
#         bot.send_message(message.chat.id, 'Ваш номер группы: 3530904/70102')
#
#     else:
#         bot.send_message(message.chat.id, 'Такого номера группы не существует')

# r = requests.get(f'{MAIN_URL}/getUpdates')
#
# pprint.pprint(r.json())


if __name__ == '__main__':
    bot.polling()
