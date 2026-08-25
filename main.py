import telebot
from groq import Groq
import base64

TELEGRAM_BOT_TOKEN = "8738833023:AAHWmKpCyoIIZtsZ3SRdl13X1ZBQ5SQ6gOE"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
Siz CEFR Writing (Task 1.1 va Task 1.2) bo'yicha professional tekshiruvchisiz.
Foydalanuvchi yuborgan rasmdagi insho matnini o'qing va quyidagi qat'iy struktura bo'yicha tahlil qiling:

1. TASK TURI: Task 1.1 (Informal Email) yoki Task 1.2 (Formal Email).
2. STRUKTURA TEKSHIRUVI:
   - Greeting & Opening
   - Main News / Main Body
   - Emotion / Reaction
   - Closing & Sign-off
3. GRAMMATIKA VA PREDLOG HATOLARI:
   - Sifat va predlog birikmalarini tekshiring.
   - Topilgan xatolarni ko'rsatib, to'g'ri variantini bering.
4. YAKUNIY BAHO VA MASLAHAT.

Javobni o'zbek tilida, aniq va chiroyli formatda taqdim eting.
"""

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Salom! CEFR Writing rasmini yuboring, tahlil qilib beraman.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "Rasm qabul qilindi. Tahlil qilinmoqda...")
    
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        image_path = "user_writing.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        base64_image = encode_image(image_path)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": SYSTEM_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="qwen/qwen3.6-27b",
        )
        
        response_text = chat_completion.choices[0].message.content
        bot.reply_to(message, response_text)
        
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")

print("Bot muvaffaqiyatli ishga tushdi!")
bot.infinity_polling(timeout=10, long_polling_timeout=5)

