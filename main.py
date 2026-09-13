import os
from flask import Flask, request
import telebot

TOKEN = '8828199644:AAH8pA8dgNUHeERBh14DgyyJoj5HKvG2pMg'
RENDER_URL = 'https://h4-amza.onrender.com'
WEBHOOK_URL = f"{RENDER_URL}/{TOKEN}"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Webhook সেট করা (Gunicorn রান করলেও এটা এক্সিকিউট হবে)
try:
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print("Webhook successfully set!")
except Exception as e:
    print(f"Error setting webhook: {e}")

# কমান্ড ও ইকো হ্যান্ডলার
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! Webhook দিয়ে বট একদম ঠিকঠাক কাজ করছে!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"আপনি বলেছেন: {message.text}")

# Telegram Webhook Endpoint
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

# Root Page Test
@app.route('/')
def index():
    return "Bot Server is Alive & Running!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

