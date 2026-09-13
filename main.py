import os
from flask import Flask, request
import telebot

# আপনার বটের টোকেন এবং Render URL
TOKEN = '8828199644:AAH8pA8dgNUHeERBh14DgyyJoj5HKvG2pMg'
RENDER_URL = 'https://ahadorg.onrender.com'  # প্রয়োজন অনুযায়ী আপনার সঠিক URL দিন
WEBHOOK_URL = f"{RENDER_URL}/{TOKEN}"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# বটের কমান্ড ও মেসেজ হ্যান্ডলার
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! Webhook দিয়ে বট সফলভাবে চালু হয়েছে।")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"আপনি পাঠিয়েছেন: {message.text}")

# Webhook Endpoint (টেলিগ্রাম এখানে মেসেজ পাঠাবে)
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

# স্বাস্থ্য পরীক্ষার জন্য রুট পেজ
@app.route('/')
def index():
    return "Bot Server is Alive and Running!", 200

# Render সার্ভার চালু হলে Webhook অটোমেটিক সেট হবে
with app.app_context():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

