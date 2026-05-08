import telebot
import requests
import os
from flask import Flask
from threading import Thread

# 1. ቦት ዝግጅት
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask('')
@app.route('/')
def home(): return "Zeky AI is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run).start()

# ሰላምታ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! እኔ Zeky AI ነኝ። አሁን ዝግጁ ነኝ፣ ማንኛውንም ነገር ጠይቁኝ!")

# ዋናው የንግግር ክፍል
@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    user_input = message.text

    # ምስል ለመፍጠር ከሆነ
    image_keywords = ["ሳልልኝ", "አሳይኝ", "ምስል", "draw", "image"]
    if any(word in user_input.lower() for word in image_keywords):
        image_url = f"https://pollinations.ai/p/{user_input.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
        bot.send_photo(message.chat.id, image_url, caption="ይኸው የጠየቅከው ምስል!")
        return

    try:
        # በጣም ፈጣን የሆነ AI መጥራት (ያለ Key የሚሰራ)
        url = f"https://text.pollinations.ai/{user_input}?model=openai&system=You are Zeky AI, a smart assistant. Answer in Amharic."
        response = requests.get(url)
        
        if response.status_code == 200:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ይቅርታ፣ አሁን ትንሽ ተቸግሬያለሁ።")
            
    except Exception as e:
        bot.reply_to(message, "ስህተት ተፈጥሯል። እባክህ ቆይተህ ሞክር።")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
