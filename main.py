import telebot
import requests
import os
from flask import Flask
from threading import Thread

# 1. የቴሌግራም ቦት ዝግጅት
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

# Render እንዳይዘጋ የሚያደርግ
app = Flask('')
@app.route('/')
def home(): return "Zeky AI is Working!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! እኔ Zeky AI ነኝ። አሁን ዝግጁ ነኝ! ማንኛውንም ነገር መጠየቅ ወይም ምስል እንዲሳልልህ ማዘዝ ትችላለህ።")

@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    user_text = message.text
    
    # ምስል የመፍጠር ጥያቄ ከሆነ
    image_keywords = ["ሳልልኝ", "አሳይኝ", "ምስል", "draw", "image", "picture"]
    if any(word in user_text.lower() for word in image_keywords):
        # ጥያቄውን ወደ እንግሊዝኛ ቀይረን ለምስል መፍጠሪያው እንልካለን
        image_url = f"https://pollinations.ai/p/{user_text.replace(' ', '%20')}?width=1080&height=1080&model=flux"
        bot.send_photo(message.chat.id, image_url, caption="ይኸው የጠየቅከው ምስል!")
        return

    try:
        # ለ AIው መልእክት መላክ (ያለ API Key የሚሰራ)
        # እዚህ ጋር Zeky AI መሆኑን እናስተምረዋለን
        system_prompt = "You are Zeky AI, a smart assistant who knows about health and education. Answer in Amharic. User says: "
        api_url = f"https://text.pollinations.ai/{system_prompt}{user_text}"
        
        response = requests.get(api_url)
        bot.reply_to(message, response.text)
        
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ አሁንም ትንሽ ችግር አለ። ቆይቼ እሞክራለሁ።")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
