
import telebot
from telebot import types

TOKEN = '7972933627:AAH4obelm7ftadnjlaQV9V5z87Jt3M6coxw'
bot = telebot.TeleBot(TOKEN)

LANGUAGES = {
    'az': '🇦🇿 Azərbaycan',
    'en': '🇬🇧 English',
    'ru': '🇷🇺 Русский'
}

# Dil seçimi
languages = {'az': 'Azərbaycan dili', 'en': 'English', 'ru': 'Русский'}

# Başlanğıc mesajı
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Xoş gəlmisiniz! Dil seçmək üçün /dil komandasını istifadə edin.")

# Dil seçimi
@bot.message_handler(commands=['dil'])
def select_language(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    for code, lang in languages.items():
        markup.add(telebot.types.KeyboardButton(lang))
    bot.send_message(message.chat.id, "Dil seçin:", reply_markup=markup)

# Dil seçimi sonrası mesaj
@bot.message_handler(func=lambda message: message.text in languages.values())
def language_response(message):
    selected_language = [code for code, lang in languages.items() if lang == message.text][0]
    bot.send_message(message.chat.id, f"Seçdiyiniz dil: {languages[selected_language]}")

# Sənəd qəbul etmək
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Faylı saxlayın
    with open(f"downloads/{message.document.file_name}", 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.send_message(message.chat.id, "Sənəd uğurla qəbul edildi!")

# Adminə bildiriş göndərmək
@bot.message_handler(commands=['notify_admin'])
def notify_admin(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "Admin, bot işləyir!")
    else:
        bot.send_message(message.chat.id, "Sadəcə admin bu əmri istifadə edə bilər.")

# Podratçılar üçün müqavilə sənədləri
@bot.message_handler(commands=['upload_contract'])
def upload_contract(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Podratçılar üçün müqavilə sənədini yükləyin.")
        # Burada sənəd yükləmək üçün əlavə funksionallıq əlavə oluna bilər

# Admin panel
@bot.message_handler(commands=['admin_panel'])
def admin_panel(message):
    if message.chat.id == ADMIN_ID:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        markup.add(telebot.types.KeyboardButton("Müqavilə Yüklə"), telebot.types.KeyboardButton("İstifadəçi Sorğusu"))
        bot.send_message(message.chat.id, "Admin Paneli: Seçiminizi edin", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Siz admin deyilsiniz.")

# Podratçılara qeydiyyat (sənəd yükləmək üçün)
@bot.message_handler(commands=['contract_registration'])
def contract_registration(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "Podratçı qeydiyyatı üçün sənədinizi göndərin.")
        # Burada sənəd qeydiyyatı üçün daha da əlavə funksionallıq əlavə edilə bilər

# Müştərilərlə əlaqə
@bot.message_handler(commands=['customer_support'])
def customer_support(message):
    bot.send_message(message.chat.id, "Müştəri dəstəyi ilə əlaqə saxlayın. Sualınızı yazın.")

# Hər hansı bir mesajı cavablandırmaq
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Sizə göstərilən mesaj: {message.text}")

# Botu işə salmaq
bot.polling(none_stop=True)

