import os
import telebot
from telebot import types

bot = telebot.TeleBot('7811689736:AAH6fowvyNk2rGeEltS0QCYAO9KbTLgXQt8')

matrix=[['k', 'i', 'v', 'Я', 'ю', 'ж', 'Ы', 'М', 'M', 'У', 'ы', 'j', 'Э', '6', "'", '4', 'Т', 'D', 'г', '=', 'w', 'n', 'ш'],
        ['Л', 'V', 'F', 'В', 'я', '1', 'S', 'т', 'ф', 'м', 'ё', 'Q', 'у', 'а', 'э', '}', 'q', 'm', '>', 'к', 'ъ', '@', 'N'],
        ['o', '&', '2', ',', ';', 'Й', 'Y', '{', 'Ф', 'Н', 'C', 'I', 'Ц', 'H', 'д', '+', 'u', 'И', '0', 'в', ')', ']', 'J'],
        ['*', '`', 'c', 'р', 'х', 'e', 'Ч', 'U', 't', 'п', 'Ъ', 'g', '%', '(', 'А', 'ц', '.', 'Ш', 'л', 'T', 'E', 'б', 'X'],
        ['f', 'н', 'z', 'K', 'G', '#', 'L', 'h', 'Ь', '_', 's', 'З', 'Б', 'щ', '|', 'О', 'ь', '<', '7', 'С', 'з', 'Ю', '?'],
        ['^', "'", 'Щ', 'y', 'Е', 'd', 'Р', ' ', '9', '8', 'ч', 'Х', 'К', 'е', '$', 'p', 'Г', 'W', 'Ж', 'A', 'O', 'x', 'Ё'],
        [':', 'и', 'й', '3', 'B', '!', 'l', 'П', '5', 'Z', 'с', '[', 'a', 'о', '\\', 'r', 'P', 'b', '~', 'R', '-', '/', 'Д']]

commands,modify=('Зашифровать','Расшифровать'),0

def getIndex(symbol):
    index=[]
    for i in range(7):
        if symbol in matrix[i]:
            index.append(i)
            index.append(matrix[i].index(symbol))
        else: continue
    if index==[]:
        return -1
    return index

def getKey(message):
    if message[-5] == " " : message_key = message[-4:]
    else: message_key = message[-5:]
    return message_key

def getVector(message_key):
    vector_modificators,vector_angle,vector = (-1, 1, 1, -1),("U","D","R","L"),[]
    if message_key[0] not in vector_angle or message_key[2] not in vector_angle:return -1
    if int(message_key[1])<=7 and int(message_key[3:])<=23:
        vector.append(int(message_key[1]) * vector_modificators[vector_angle.index(message_key[0])])
        vector.append(int(message_key[3:]) * vector_modificators[vector_angle.index(message_key[2])])
    else:
        return -1
    return vector

def encodeOrDecode(message,radio_modificator):
    modified_message = ""
    if len(message)<5: return -1
    if getVector(getKey(message))==-1: return -1
    for i in range(len(message)-len(getKey(message))-1):
        modified_index0 = (getIndex(message[i])[0]+radio_modificator*getVector(getKey(message))[0])%7
        modified_index1 = (getIndex(message[i])[1]+radio_modificator*getVector(getKey(message))[1])%23
        modified_message+=matrix[modified_index0][modified_index1]
    return modified_message

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Зашифровать")
    btn2 = types.KeyboardButton("Расшифровать")
    markup.add(btn1,btn2)
    bot.send_message(message.from_user.id, "Выбери опцию", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global modify
    n=0
    if message.text == 'Зашифровать':
        modify = 1
        bot.send_message(message.from_user.id, 'Введи сообщение для зашифровки (ключ вводится через пробел в конце сообщения)', parse_mode='Markdown')

    elif message.text == 'Расшифровать':
        modify = -1
        bot.send_message(message.from_user.id, 'Введи сообщение для расшифровки (ключ вводится через пробел в конце сообщения)', parse_mode='Markdown')

    elif message.text not in commands:
        for i in range(len(message.text)):
            if getIndex(message.text[i]) == -1:
                bot.send_message(message.from_user.id, 'Ошибка ввода: Недопустимый символ', parse_mode='Markdown')
            elif n<1:
                n+=1
                if type(encodeOrDecode(message.text, modify))!=int:bot.send_message(message.from_user.id,"Измененное сообщение: "+encodeOrDecode(message.text, modify)+" , Ключ: "+getKey(message.text), parse_mode='Markdown')
                elif encodeOrDecode(message.text, modify)==-1:bot.send_message(message.from_user.id,"Ошибка: Отсутствует ключ или он некорректен",parse_mode='Markdown')

    else:bot.send_message(message.from_user.id,"Ошибка ввода команды")


bot.polling(none_stop=True, interval=0)
