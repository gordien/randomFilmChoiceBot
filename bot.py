import telebot
import db as pg
import kpadapter
import config


TOKEN = "2110122103:AAERC4s9rn6sRUXFAhNv61Y7aCB5dazMlcQ"

bot = telebot.TeleBot(TOKEN)


def check_user(message):
    return message.from_user.id in config.users

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    if check_user(message):
        bot.send_message(message.chat.id, f"Отправьте ссылку на фильм на кинопоиске для добавления в список")
    else:
        bot.send_message(message.chat.id, f"private data")


@bot.message_handler(commands=['random'])
def get_film_list(message):
    if check_user(message):
        bot.send_message(message.chat.id, pg.get_film_list(message.from_user.id))
    else:
        bot.send_message(message.chat.id, f"private data")


@bot.message_handler(commands=['list'])
def get_film_list(message):
    if check_user(message):
        bot.send_message(message.chat.id, pg.get_film_list())
    else:
        bot.send_message(message.chat.id, f"private data")

@bot.message_handler(content_types=['text'])
def parse_message(message):
    if check_user(message):
        try:
            pg.add_film_to_list_db(kpadapter.save_film_info_url(message.text),message.from_user.id)
            bot.send_message(message.chat.id, 'Фильм добавлен в список. Для просомтра списка выполните команду /list')
        except Exception as e:
            print(e)
    else:
        bot.send_message(message.chat.id, f"private data")




bot.polling(none_stop=True)



