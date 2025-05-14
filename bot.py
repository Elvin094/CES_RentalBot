# -*- coding: utf-8 -*-
import telebot
import os
import sqlite3
from telebot import types
from datetime import datetime

BOT_TOKEN = "7972933627:AAH4obelm7ftadnjlaQV9V5z87Jt3M6coxw"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 1341932557  # Öz Telegram ID-ni yaz

conn = sqlite3.connect("orders.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    message TEXT,
    created_at TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    filename TEXT,
    created_at TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    filename TEXT,
    created_at TEXT
)
""")
conn.commit()

user_lang = {}

LANGS = {
    "az": {
        "language_selected": "✅ Dil: Azərbaycan",
        "welcome": "CES RentalBot-a xoş gəlmisiniz! Rolunuzu seçin:",
        "customer": "👷 Müştəri",
        "contractor": "🏗️ Podratçı",
        "admin": "🛠 Admin Panel (Yalnız Admin üçün)",
        "tech_list": "🔧 Mövcud texnikalar:\n- JCB 540-140\n- Manitou MT932\n- Forklift 3.5T",
        "delivery": "🚚 Daşınma sifarişi üçün məlumatları yazın.",
        "upload_doc": "📎 Rekvizit sənədinizi PDF şəklində göndərin.",
        "send_contract": "📑 Müqavilə sənədi: https://sizin-sayt.com/muqavile.pdf",
        "send_equipment": "📤 Texnika məlumat və şəkillərini göndərin.",
        "admin_docs": "📂 Gələn sənədlər:",
        "no_docs": "Qeyd yoxdur.",
        "order_saved": "✅ Sifariş qeydə alındı!",
        "photo_saved": "✅ Şəkil yükləndi!",
        "doc_saved": "✅ Sənəd qəbul olundu!",
        "thanks": "🙏 Təşəkkür edirik!",
        "back": "⬅️ Geri",
        "show_orders": "📊 Sifarişlər",
        "show_docs": "📁 Sənədlər",
        "show_photos": "🖼 Şəkillər"
    },
    "en": {
        "language_selected": "✅ Language: English",
        "welcome": "Welcome to CES RentalBot! Please choose your role:",
        "customer": "👷 Customer",
        "contractor": "🏗️ Contractor",
        "admin": "🛠 Admin Panel (Admin only)",
        "tech_list": "🔧 Available Equipment:\n- JCB 540-140\n- Manitou MT932\n- Forklift 3.5T",
        "delivery": "🚚 Please send delivery request details.",
        "upload_doc": "📎 Please upload your requisites in PDF.",
        "send_contract": "📑 Contract link: https://sizin-sayt.com/muqavile.pdf",
        "send_equipment": "📤 Send equipment photo and details.",
        "admin_docs": "📂 Received documents:",
        "no_docs": "No records found.",
        "order_saved": "✅ Order received!",
        "photo_saved": "✅ Photo uploaded!",
        "doc_saved": "✅ Document received!",
        "thanks": "🙏 Thank you!",
        "back": "⬅️ Back",
        "show_orders": "📊 View Orders",
        "show_docs": "📁 View Documents",
        "show_photos": "🖼 View Photos"
    },
    "ru": {
        "language_selected": "✅ Язык: Русский",
        "welcome": "Добро пожаловать в CES RentalBot! Пожалуйста, выберите вашу роль:",
        "customer": "👷 Клиент",
        "contractor": "🏗️ Подрядчик",
        "admin": "🛠 Админ Панель (только для Админа)",
        "tech_list": "🔧 Доступная техника:\n- JCB 540-140\n- Manitou MT932\n- Погрузчик 3.5T",
        "delivery": "🚚 Пожалуйста, отправьте данные для доставки.",
        "upload_doc": "📎 Отправьте реквизиты в PDF.",
        "send_contract": "📑 Ссылка на договор: https://sizin-sayt.com/muqavile.pdf",
        "send_equipment": "📤 Отправьте фото и данные техники.",
        "admin_docs": "📂 Полученные документы:",
        "no_docs": "Нет записей.",
        "order_saved": "✅ Заказ принят!",
        "photo_saved": "✅ Фото загружено!",
        "doc_saved": "✅ Документ принят!",
        "thanks": "🙏 Спасибо!",
        "back": "⬅️ Назад",
        "show_orders": "📊 Заказы",
        "show_docs": "📁 Документы",
        "show_photos": "🖼 Фото"
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🇦🇿 Azərbaycan dili", "🇷🇺 Русский", "🇬🇧 English")
    bot.send_message(
        message.chat.id,
        "🌐 Zəhmət olmasa dili seçin:\n\n🇦🇿 Azərbaycan dili\n🇷🇺 Русский\n🇬🇧 English",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text in ["🇦🇿 Azərbaycan dili", "🇷🇺 Русский", "🇬🇧 English"])
def select_language(message):
    lang_code = {
        "🇦🇿 Azərbaycan dili": "az",
        "🇷🇺 Русский": "ru",
        "🇬🇧 English": "en"
    }[message.text]

    user_lang[message.chat.id] = lang_code
    l = LANGS[lang_code]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(l["customer"] + " – Rol", l["contractor"] + " – Rol")
    if message.chat.id == ADMIN_ID:
        markup.add(l["admin"] + " – Rol")

    bot.send_message(
        message.chat.id,
        l["language_selected"] + "\n\n" + l["welcome"],
        reply_markup=markup
    )

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    lang = user_lang.get(message.chat.id, 'az')
    l = LANGS[lang]
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    os.makedirs("profile_photos", exist_ok=True)
    filename = f"profile_photos/{message.chat.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    cursor.execute("INSERT INTO photos (user_id, filename, created_at) VALUES (?, ?, ?)",
                   (message.chat.id, filename, datetime.now().isoformat()))
    conn.commit()
    bot.send_message(message.chat.id, l["photo_saved"])
    bot.send_message(message.chat.id, l["thanks"])

@bot.message_handler(content_types=['document'])
def handle_document(message):
    lang = user_lang.get(message.chat.id, 'az')
    l = LANGS[lang]
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    os.makedirs("documents", exist_ok=True)
    file_path = f"documents/{message.document.file_name}"
    with open(file_path, "wb") as f:
        f.write(downloaded_file)
    cursor.execute("INSERT INTO documents (user_id, filename, created_at) VALUES (?, ?, ?)",
                   (message.chat.id, message.document.file_name, datetime.now().isoformat()))
    conn.commit()
    bot.send_message(message.chat.id, l["doc_saved"])
    bot.send_message(message.chat.id, l["thanks"])

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    lang = user_lang.get(message.chat.id, 'az')
    l = LANGS[lang]
    uid = message.chat.id
    text = message.text

    if l["customer"] in text:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📋 " + l["tech_list"], "🚚 " + l["delivery"], l["back"])
        bot.send_message(uid, l["welcome"], reply_markup=markup)
    elif l["contractor"] in text:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📤 " + l["send_equipment"], "📎 " + l["upload_doc"], "📑 " + l["send_contract"], l["back"])
        bot.send_message(uid, l["welcome"], reply_markup=markup)
    elif l["admin"] in text and uid == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(l["show_orders"], l["show_docs"], l["show_photos"], l["back"])
        bot.send_message(uid, l["welcome"], reply_markup=markup)
    elif text == "📋 " + l["tech_list"]:
        bot.send_message(uid, l["tech_list"])
    elif text == "🚚 " + l["delivery"]:
        bot.send_message(uid, l["delivery"])
    elif text == "📎 " + l["upload_doc"]:
        bot.send_message(uid, l["upload_doc"])
    elif text == "📑 " + l["send_contract"]:
        bot.send_message(uid, l["send_contract"])
    elif text == "📤 " + l["send_equipment"]:
        bot.send_message(uid, l["send_equipment"])
    elif text == l["show_orders"] and uid == ADMIN_ID:
        cursor.execute("SELECT username, message, created_at FROM orders ORDER BY created_at DESC LIMIT 10")
        rows = cursor.fetchall()
        reply = "\n\n".join([f"👤 @{row[0]}\n📨 {row[1]}\n🕓 {row[2]}" for row in rows]) if rows else l["no_docs"]
        bot.send_message(uid, reply)
    elif text == l["show_docs"] and uid == ADMIN_ID:
        cursor.execute("SELECT filename, created_at FROM documents ORDER BY created_at DESC LIMIT 10")
        rows = cursor.fetchall()
        reply = "\n".join([f"📎 {row[0]} - {row[1]}" for row in rows]) if rows else l["no_docs"]
        bot.send_message(uid, reply)
    elif text == l["show_photos"] and uid == ADMIN_ID:
        cursor.execute("SELECT filename, created_at FROM photos ORDER BY created_at DESC LIMIT 5")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                with open(row[0], 'rb') as photo:
                    bot.send_photo(uid, photo, caption=row[1])
        else:
            bot.send_message(uid, l["no_docs"])
    elif text == l["back"]:
        start(message)
    else:
        cursor.execute("INSERT INTO orders (user_id, username, message, created_at) VALUES (?, ?, ?, ?)",
                       (uid, message.from_user.username, text, datetime.now().isoformat()))
        conn.commit()
        bot.send_message(uid, l["order_saved"])
        bot.send_message(uid, l["thanks"])
        bot.send_message(ADMIN_ID, f"📦 Yeni sifariş:\nGöndərən: @{message.from_user.username}\n📨 Məzmun: {text}")

bot.polling(none_stop=True)
