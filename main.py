import os
import logging
from flask import Flask, request
import telebot

# Logging চালু করা যাতে যেকোনো সমস্যা ব্যাকএন্ডে স্পষ্ট দেখা যায়
logging.basicConfig(level=logging.INFO)

TOKEN = '8828199644:AAH8pA8dgNUHeERBh14DgyyJoj5HKvG2pMg'
RENDER_URL = 'https://h4-amza.onrender.com'
WEBHOOK_URL = f"{RENDER_URL}/{TOKEN}"

bot = telebot.TeleBot(TOKEN, threaded=False)  # Threaded=False দিলে Synchronous প্রসেসিং নিশ্চিত হয়
app = Flask(__name__)

# ১. কমান্ড ও মেসেজ হ্যান্ডলার
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        bot.reply_to(message, "হ্যালো! Webhook একদম সফলভাবে কাজ করছে।")
    except Exception as e:
        print(f"Error sending message: {e}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.reply_to(message, f"আপনি লিখেছেন: {message.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

# ২. অ্যাডভান্সড Webhook Endpoint
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        try:
            # Raw string ডাটা পড়া
            json_string = request.get_data().decode('utf-8')
            
            # telebot-এর স্ট্রিক্ট JSON পার্সার ব্যবহার করা (এটিই আসল ফিক্স)
            update = telebot.types.Update.de_json(json_string)
            
            # যদি পার্সিং ব্যর্থ না হয়, আপডেট প্রসেস করা
            if update:
                bot.process_new_updates([update])
            return 'OK', 200
        except Exception as e:
            print(f"Webhook processing error: {e}")
            return 'Error', 500
    return 'Forbidden', 403

# ৩. হেলথ চেক রুট
@app.route('/')
def index():
    return "Bot Server is Healthy and Live!", 200

# ৪. অ্যাপ চালুর সময় Webhook সক্রিয় করা
try:
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(">>> Webhook setup successfully completed! <<<")
except Exception as e:
    print(f">>> Webhook setup failed: {e} <<<")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

