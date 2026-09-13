import os
import logging
from flask import Flask, request
import telebot
from telebot import types

logging.basicConfig(level=logging.INFO)

TOKEN = '8828199644:AAH8pA8dgNUHeERBh14DgyyJoj5HKvG2pMg'
RENDER_URL = 'https://h4-amza.onrender.com'
WEBHOOK_URL = f"{RENDER_URL}/{TOKEN}"

ADMIN_ID = 8768764605  # আপনার এডমিন আইডি

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# ==================== DYNAMIC DATABASE (IN-MEMORY) ====================
# চ্যানেল লিংক
config_channels = [
    {"name": "🔊 Join Channel 1 ↗️", "url": "https://t.me/RB_Python_Bot_Host_BD", "username": "@RB_Python_Bot_Host_BD"},
    {"name": "🔊 Join Channel 2 ↗️", "url": "https://t.me/RB_Bot_Host_BD_Updates", "username": "@RB_Bot_Host_BD_Updates"}
]

# বাটনের কাস্টমাইজড মেসেজ ও ইনলাইন বাটন ডাটাবেজ
button_responses = {
    "💎 ফ্রি হোস্ট": {
        "text": "🆓 <b>ফ্রি হোস্টিং:</b>\nআপনার বট ফাইল (.py / .js) আপলোড করতে '🚀 ফাইল আপলোড' বাটনে চাপুন।",
        "inline_btn": {"text": "📤 ফাইল আপলোড নির্দেশিকা", "url": "https://t.me/RB_Python_Bot_Host_BD"}
    },
    "💳 প্ল্যান কিনুন": {
        "text": "💳 <b>প্রিমিয়াম প্ল্যানসমূহ:</b>\n\n১. VIP Plan - ৫০ টাকা/মাস\n২. Ultra Plan - ১০০ টাকা/মাস",
        "inline_btn": {"text": "💬 এডমিনের সাথে কথা বলুন", "url": "https://t.me/RB_Support_Bot"}
    },
    "🚀 ফাইল আপলোড": {"text": "📤 আপনার Python (.py) অথবা Node.js (.js) ফাইলটি চ্যাটে পাঠান।", "inline_btn": None},
    "📁 প্রজেক্ট ম্যানেজ": {"text": "📁 আপনার কোনো সক্রিয় প্রজেক্ট নেই।", "inline_btn": None},
    "🎧 সাপোর্ট": {"text": "🎧 যেকোনো প্রয়োজনে আমাদের সাপোর্ট চ্যাটে মেসেজ দিন।", "inline_btn": {"text": "🎧 Support Group", "url": "https://t.me/RB_Support_Bot"}},
    "📢 আপডেটসে": {"text": "📢 সব নতুন আপডেট পেতে আমাদের চ্যানেলে চোখ রাখুন!", "inline_btn": None},
    "👤 অ্যাকাউন্ট": {"text": "👤 <b>ইউজার প্রোফাইল:</b>\nস্ট্যাটাস: Free User", "inline_btn": None},
    "🌐 ভাষা": {"text": "🌐 বর্তমানে শুধুমাত্র <b>বাংলা</b> ভাষা সমর্থিত।", "inline_btn": None},
    "📊 বট স্ট্যাটাস": {"text": "📊 <b>সার্ভার স্ট্যাটাস:</b>\nServer Status: Online 🟢", "inline_btn": None},
    "⚡ স্পিড ও পিং": {"text": "⚡ <b>Ping:</b> 42ms\nServer Speed: 100 Mbps 🚀", "inline_btn": None}
}

user_states = {}  # এডমিন ইনপুট ট্র্যাক করার জন্য

# ==================== HELPER FUNCTIONS ====================
def check_must_join(user_id):
    for ch in config_channels:
        if ch.get("username"):
            try:
                member = bot.get_chat_member(ch["username"], user_id)
                if member.status in ['left', 'kicked']:
                    return False
            except Exception:
                pass
    return True

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(k) for k in button_responses.keys()]
    for i in range(0, len(buttons), 2):
        markup.add(*buttons[i:i+2])
    return markup

def join_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for ch in config_channels:
        markup.add(types.InlineKeyboardButton(ch["name"], url=ch["url"]))
    markup.add(types.InlineKeyboardButton("✅ I Joined ✅", callback_data="check_joined"))
    return markup

# ==================== USER HANDLERS ====================
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    if not check_must_join(user_id):
        join_msg = "📢 <b>আমাদের চ্যানেলগুলোতে জয়েন করুন!</b>\n\nবট ব্যবহার করতে নিচের সব চ্যানেলে জয়েন করা প্রয়োজন:"
        bot.send_message(message.chat.id, join_msg, parse_mode='HTML', reply_markup=join_keyboard())
        return

    first_name = message.from_user.first_name
    welcome_msg = (
        f"🎉 <b>অভিনন্দন!</b> 🎉\n"
        f"═════════════════════════════\n"
        f"✨ <b>স্বাগতম, {first_name}'s!</b>\n"
        f"═════════════════════════════\n\n"
        f"🆔 <b>আপনার আইডি:</b> <code>{user_id}</code>\n"
        f"🟢 <b>স্ট্যাটাস:</b> 🆓 No Active Plan\n"
        f"📁 <b>প্রজেক্ট:</b> 0 / 0\n"
        f"═════════════════════════════\n\n"
        f"🤖 সম্পূর্ণ ফ্রিতে আপনার বট হোস্ট করুন!\n"
        f"আপনার Python (.py) ও JS (.js) বট ২৪/৭ চালু রাখুন।\n\n"
        f"👇 <b>নিচের মেনু থেকে বেছে নিন:</b>"
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode='HTML', reply_markup=main_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "check_joined")
def check_join_callback(call):
    if check_must_join(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ জয়েনিং যাচাই সফল হয়েছে!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start_command(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ আপনি এখনো সবগুলো চ্যানেলে জয়েন করেননি!", show_alert=True)

# ==================== ADMIN PANEL HANDLERS ====================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("⚙️ চ্যানেল লিংক পরিবর্তন করুন", callback_data="admin_edit_channels"),
        types.InlineKeyboardButton("📝 বাটন মেসেজ ও ইনলাইন বাটন কাস্টমাইজ", callback_data="admin_select_button")
    )
    bot.send_message(message.chat.id, "🛠 <b>এডমিন প্যানেলে স্বাগতম:</b>\nনিচের অপশন থেকে সিলেক্ট করুন:", parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def admin_callbacks(call):
    if call.from_user.id != ADMIN_ID:
        return

    data = call.data
    chat_id = call.message.chat.id

    if data == "admin_edit_channels":
        msg = "নতুন চ্যানেল সেট করতে নিচের ফরম্যাটে ডাটা পাঠাতেন:\n\n`লিংক১, @ইউজারনেম১ | লিংক২, @ইউজারনেম২`\n\nউদাহরণ:\n`https://t.me/mych1, @mych1 | https://t.me/mych2, @mych2`"
        user_states[ADMIN_ID] = "WAITING_CHANNELS"
        bot.send_message(chat_id, msg, parse_mode='Markdown')

    elif data == "admin_select_button":
        markup = types.InlineKeyboardMarkup(row_width=2)
        for btn_name in button_responses.keys():
            markup.add(types.InlineKeyboardButton(btn_name, callback_data=f"edit_btn_{btn_name}"))
        bot.send_message(chat_id, "যে বাটন কাস্টমাইজ করতে চান সেটি বেছে নিন:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("edit_btn_"))
def edit_button_callback(call):
    if call.from_user.id != ADMIN_ID:
        return
    btn_name = call.data.replace("edit_btn_", "")
    user_states[ADMIN_ID] = f"WAITING_MSG_{btn_name}"
    
    msg = (
        f"<b>'{btn_name}'</b> বাটনের নতুন মেসেজ ও ইনলাইন বাটন সেট করুন।\n\n"
        f"ফরম্যাট:\n<code>মেসেজ টেক্সট | ইনলাইন বাটনের নাম | ইনলাইন বাটনের লিংক</code>\n\n"
        f"উদাহরণ (ইনলাইন বাটনসহ):\n<code>নতুন অফার দেখুন! | অফার লিংক | https://t.me/example</code>\n\n"
        f"উদাহরণ (ইনলাইন বাটন ছাড়া):\n<code>শুধু টেক্সট মেসেজ পাঠাতে চান</code>"
    )
    bot.send_message(call.message.chat.id, msg, parse_mode='HTML')

# ==================== MAIN MESSAGE DISPATCHER ====================
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    text = message.text

    # ১. এডমিন স্টেট চেক (ডাটা আপডেট করার জন্য)
    if user_id == ADMIN_ID and user_id in user_states:
        state = user_states[user_id]
        
        # চ্যানেল আপডেট
        if state == "WAITING_CHANNELS":
            try:
                global config_channels
                new_channels = []
                parts = text.split("|")
                for i, part in enumerate(parts):
                    url, uname = part.strip().split(",")
                    new_channels.append({
                        "name": f"🔊 Join Channel {i+1} ↗️",
                        "url": url.strip(),
                        "username": uname.strip()
                    })
                config_channels = new_channels
                bot.reply_to(message, "✅ ফোর্স চ্যানেল সফলভাবে আপডেট করা হয়েছে!")
            except Exception as e:
                bot.reply_to(message, f"❌ ভুল ফরম্যাট! আবার চেষ্টা করুন। Error: {e}")
            del user_states[user_id]
            return

        # বাটন মেসেজ ও ইনলাইন বাটন আপডেট
        elif state.startswith("WAITING_MSG_"):
            btn_name = state.replace("WAITING_MSG_", "")
            try:
                parts = text.split("|")
                new_text = parts[0].strip()
                inline_data = None
                
                if len(parts) >= 3:
                    inline_data = {"text": parts[1].strip(), "url": parts[2].strip()}
                
                button_responses[btn_name] = {
                    "text": new_text,
                    "inline_btn": inline_data
                }
                bot.reply_to(message, f"✅ <b>'{btn_name}'</b> বাটনের মেসেজ ও ইনলাইন বাটন আপডেট হয়েছে!", parse_mode='HTML')
            except Exception as e:
                bot.reply_to(message, f"❌ ভুল ফরম্যাট! Error: {e}")
            del user_states[user_id]
            return

    # ২. চ্যানেল জয়েন ফিল্টার (সাধারণ ইউজারদের জন্য)
    if not check_must_join(user_id):
        join_msg = "📢 <b>আমাদের চ্যানেলগুলোতে জয়েন করুন!</b>\n\nবট ব্যবহার করতে নিচের সব চ্যানেলে জয়েন করা প্রয়োজন:"
        bot.send_message(message.chat.id, join_msg, parse_mode='HTML', reply_markup=join_keyboard())
        return

    # ৩. সাধারণ কিবোর্ড ক্লিক রেসপন্স
    if text in button_responses:
        btn_data = button_responses[text]
        markup = None
        
        # ইনলাইন বাটন থাকলে তা যোগ করা
        if btn_data.get("inline_btn"):
            markup = types.InlineKeyboardMarkup()
            ib = btn_data["inline_btn"]
            markup.add(types.InlineKeyboardButton(ib["text"], url=ib["url"]))
            
        bot.send_message(message.chat.id, btn_data["text"], parse_mode='HTML', reply_markup=markup)

# ==================== WEBHOOK & SERVER ROUTING ====================
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
            print(f"Webhook error: {e}")
            return 'Error', 500
    return 'Forbidden', 403

@app.route('/')
def index():
    return "Dynamic Admin Bot Server Active!", 200

try:
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(">>> Webhook Connected! <<<")
except Exception as e:
    print(f">>> Webhook Error: {e} <<<")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

