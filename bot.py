import telebot
import os
import sqlite3
from telebot import types
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 1341932557  # Öz Telegram ID-ni buraya əlavə et

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
        "welcome": "CES RentalBot-a xoş gəlmisiniz! Zəhmət olmasa istifadəçi növünü seçin:",
        "customer": "👷 Müştəri",
        "contractor": "🏗️ Podratçı",
        "admin": "🛠 Admin Panel",
        "tech_list": "🔧 Mövcud texnikalar:\n- JCB 540-140\n- Manitou MT932\n- Forklift 3.5T",
        "delivery": "🚚 Daşınma sifarişi üçün zəhmət olmasa məlumatları göndərin.",
        "upload_doc": "📎 Rekvizit sənədinizi PDF formatda göndərin.",
        "send_contract": "📑 Müqavilə sənədini yükləmək üçün link: https://sizin-sayt.com/muqavile.pdf",
        "send_equipment": "📤 Texnikanın şəkil və məlumatlarını göndərin.",
        "admin_docs": "📂 Gələn sənədlər:",
        "no_docs": "Heç bir sənəd daxil olmayıb.",
        "order_saved": "✅ Sifarişiniz qeydə alındı!",
        "photo_saved": "✅ Şəkil uğurla yükləndi!",
        "back": "⬅️ Geri",
        "show_orders": "📊 Sifarişləri Göstər",
        "show_docs": "📁 Sənədləri Göstər",
        "show_photos": "🖼 Şəkilləri Göstər"
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👷 Müştəri", "🏗️ Podratçı")
    if message.chat.id == ADMIN_ID:
        markup.add("🛠 Admin Panel")
    user_lang[message.chat.id] = "az"
    bot.send_message(message.chat.id, LANGS["az"]["welcome"], reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    os.makedirs("profile_photos", exist_ok=True)
    filename = f"profile_photos/{message.chat.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    cursor.execute("INSERT INTO photos (user_id, filename, created_at) VALUES (?, ?, ?)",
                   (message.chat.id, filename, datetime.now().isoformat()))
    conn.commit()
    bot.send_message(message.chat.id, LANGS["az"]["photo_saved"])

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    os.makedirs("documents", exist_ok=True)
    file_path = f"documents/{message.document.file_name}"
    with open(file_path, "wb") as f:
        f.write(downloaded_file)
    cursor.execute("INSERT INTO documents (user_id, filename, created_at) VALUES (?, ?, ?)",
                   (message.chat.id, message.document.file_name, datetime.now().isoformat()))
    conn.commit()
    bot.send_message(message.chat.id, "✅ Sənəd qəbul edildi.")

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    uid = message.chat.id
    text = message.text
    l = LANGS["az"]

    if text == l["customer"]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📋", "🚚", l["back"])
        bot.send_message(uid, l["welcome"], reply_markup=markup)
    elif text == l["contractor"]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📤", "📎", "📑", l["back"])
        bot.send_message(uid, l["welcome"], reply_markup=markup)
    elif text == l["admin"] and uid == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📥", "➕", l["show_orders"], l["show_docs"], l["show_photos"], l["back"])
        bot.send_message(uid, l["welcome"], reply_markup=markup)
    elif text == "📋":
        bot.send_message(uid, l["tech_list"])
    elif text == "🚚":
        bot.send_message(uid, l["delivery"])
    elif text == "📎":
        bot.send_message(uid, l["upload_doc"])
    elif text == "📑":
        bot.send_message(uid, l["send_contract"])
    elif text == "📤":
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
        bot.send_message(ADMIN_ID, f"📦 Yeni sifariş:\nGöndərən: @{message.from_user.username}\n📨 Məzmun: {text}")

bot.polling(none_stop=True)
