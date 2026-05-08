import telebot
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# 1. AI Setup
# እዚህ ጋር ያወጣኸው የ Google API Key በትክክል መኖሩን አረጋግጥ
GOOGLE_API_KEY = "AIzaSyBkTnC4eHwvJsCPDt6YfyfwKqUd3wOa-Rg"
genai.configure(api_key=GOOGLE_API_KEY)

# ቦቱ ምን አይነት ባህሪ እንዲኖረው እንደምንፈልግ
instruction = "አንተ Zeky AI ነህ። በጣም ጎበዝ፣ ስለ ጤና እና ትምህርት ጥልቅ እውቀት ያለህ ረዳት ነህ። ሁልጊዜ በአማርኛ በትህትና መልስ ስጥ።"

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=instruction
)

# 2. Telegram Setup
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask('')
@app.route('/')
def home(): return "Zeky AI is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! እኔ Zeky AI ነኝ። ሁሉንም ነገር መጠየቅ ትችላለህ። ምን ልርዳህ?")

@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        # AIውን መጠየቅ
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        # ስህተቱ ምን እንደሆነ ለጥቂት ጊዜ እንዲያሳየን እዚህ ጋር እንቀይረው
        bot.reply_to(message, f"AI Error: የ Google API Key ችግር ያለ ይመስላል። እባክህ ቁልፉን ቼክ አድርግ።")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
