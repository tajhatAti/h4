import os
import logging
from flask import Flask, request
import telebot

logging.basicConfig(level=logging.INFO)

TOKEN = '8828199644:AAH8pA8dgNUHeERBh14DgyyJoj5HKvG2pMg'
RENDER_URL = 'https://h4-amza.onrender.com'
WEBHOOK_URL = f"{RENDER_URL}/{TOKEN}"

# আপনার দেওয়া নির্দিষ্ট অ্যাডমিন আইডি (Integer হিসেবে রাখা হয়েছে)
ADMIN_ID = 8768764605

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# ১. /start কমান্ডের হ্যান্ডলার
@bot.message_handler(commands=['start'])
def handle_start(message):
    # শুধু অ্যাডমিন আইডি হলেই রেসপন্স করবে
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "স্বাগতম অ্যাডমিন! বট সফলভাবে আপনার নির্দেশের জন্য প্রস্তুত।")
    # অন্য ইউজার হলে কোনো অ্যাকশন নেওয়া হবে না (Silent Ignore)

# ২. সাধারণ মেসেজ হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_admin_messages(message):
    # ইউজার আইডি চেক
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, f"স্যার, আপনার পাঠানো মেসেজ পাওয়া গেছে: {message.text}")
    # অন্য কেউ মেসেজ দিলে সম্পূর্ণ ইগনোর করবে

# Webhook Endpoint
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        try:
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            if update:
                bot.process_new_updates([update])
            return 'OK', 200
        except Exception as e:
            print(f"Webhook processing error: {e}")
            return 'Error', 500
    return 'Forbidden', 403

# Root Page
@app.route('/')
def index():
    return "Admin Only Bot Server is Active!", 200

# Webhook সেটআপ
try:
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(">>> Admin Bot Webhook Set Successfully! <<<")
except Exception as e:
    print(f">>> Webhook Setup Error: {e} <<<")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

