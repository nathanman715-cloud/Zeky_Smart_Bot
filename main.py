import telebot
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# 1. AI አእምሮ ዝግጅት
GOOGLE_API_KEY = "AIzaSyBkTnC4eHwvJsCPDt6YfyfwKqUd3wOa-Rg"
genai.configure(api_key=GOOGLE_API_KEY)

# ለ AIው 'ባህሪ' መስጠት (System Instruction)
system_instruction = (
    "አንተ Zeky AI ነህ። በጣም ጎበዝ፣ አስተዋይ እና አጋዥ የ AI ረዳት ነህ። "
    "ስለ ጤና ጥያቄዎች ስትጠየቅ በጣም ትክክለኛ እና ሳይንሳዊ መረጃዎችን ስጥ። "
    "ተጠቃሚው ምስል እንዲሳልልህ ሲጠየቅ (ለምሳሌ፡ 'የድመት ምስል ሳልልኝ') "
    "ምስሉን ለመሳል ዝግጁ መሆንህን ግለጽና የሚከተለውን ሊንክ ተጠቀም፡ "
    "https://pollinations.ai/p/[prompt_in_english] "
    "ሁልጊዜ በትህትና እና በአማርኛ በደንብ አውራ።"
)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_instruction
)

# 2. የቴሌግራም ቦት ዝግጅት
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

# Render እንዳይዘጋ የሚያደርግ
app = Flask('')
@app.route('/')
def home(): return "Zeky AI (Smart Edition) is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! እኔ Zeky AI ነኝ። ስለ ጤና፣ ስለ ትምህርት መጠየቅ ወይም ምስል እንዲሳልልህ ማዘዝ ትችላለህ። ምን ልርዳህ?")

@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    user_text = message.text
    
    # ምስል የመፍጠር ጥያቄ መሆኑን ቼክ ማድረግ
    image_keywords = ["ሳልልኝ", "አሳይኝ", "ምስል", "draw", "image", "picture"]
    is_image_request = any(word in user_text.lower() for word in image_keywords)

    try:
        response = model.generate_content(user_text)
        ai_reply = response.text

        if is_image_request:
            # AIው የተጠቃሚውን ጥያቄ ወደ እንግሊዝኛ ቀይሮ እንዲሰጠን መጠየቅ (ለሊንኩ እንዲመች)
            prompt_eng = model.generate_content(f"Translate this image prompt to a simple English description: {user_text}").text.strip()
            image_url = f"https://pollinations.ai/p/{prompt_eng.replace(' ', '%20')}"
            
            bot.send_photo(message.chat.id, image_url, caption=f"ይኸው የጠየቅከው ምስል፦\n\n{ai_reply}")
        else:
            bot.reply_to(message, ai_reply)
            
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ አሁን ትንሽ ተቸግሬያለሁ።")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
