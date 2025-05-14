
import telebot
from telebot import types

TOKEN = '7972933627:AAH4obelm7ftadnjlaQV9V5z87Jt3M6coxw'
bot = telebot.TeleBot(TOKEN)

LANGUAGES = {
    'az': '🇦🇿 Azərbaycan',
    'en': '🇬🇧 English',
    'ru': '🇷🇺 Русский'
}

# Dildə seçim
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for code, lang in LANGUAGES.items():
        markup.add(types.KeyboardButton(lang))
    msg = bot.send_message(message.chat.id, "Zəhmət olmasa dil seçin / Please choose your language / Пожалуйста, выберите язык:", reply_markup=markup)
    bot.register_next_step_handler(msg, language_selected)

def language_selected(message):
    selected_lang = message.text
    if selected_lang in LANGUAGES.values():
        bot.send_message(message.chat.id, "Dil seçildi. Bot funksiyaları aktivləşir...", reply_markup=types.ReplyKeyboardRemove())
        # Burada istifadəçi seçiminə görə dilə uyğun menyular aktiv edilə bilər
    else:
        bot.send_message(message.chat.id, "Yanlış seçim. Lütfən yenidən başlayın: /start")

bot.polling()
