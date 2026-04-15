import os
import random
import asyncio
from telegram import Bot
from openai import OpenAI

# === НАСТРОЙКИ ===
BOT_TOKEN = "8787905510:AAG4YfuFNO4R8gbLOVBJUA71nhkD_2xbl1k"
CHAT_ID = "-1003997119122"
PHOTO_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop", "tg_photos")
POST_INTERVAL = 9 * 60 * 60  # 9 часов

# OpenAI (для текста)
client = OpenAI(api_key="ТВОЙ_OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)

# === ГЕНЕРАЦИЯ ТЕКСТА ===
def generate_caption():
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Write short neutral captions for photos in a casual teenage style. No slang overload."
                },
                {"role": "user", "content": "Generate caption"}
            ],
            max_tokens=40
        )
        return response.choices[0].message.content.strip()
    except Exception:
        captions = [
            "Just another moment captured.",
            "Simple vibes, nothing special.",
            "Chill mood for today.",
            "Keeping things easy.",
            "Just a random shot."
        ]
        return random.choice(captions)

# === ПОЛУЧЕНИЕ ФОТО ===
def get_random_photo():
    if not os.path.exists(PHOTO_FOLDER):
        print("Папка не найдена:", PHOTO_FOLDER)
        return None

    files = os.listdir(PHOTO_FOLDER)
    images = [f for f in files if f.lower().endswith((".jpg", ".png", ".jpeg"))]

    if not images:
        return None

    return os.path.join(PHOTO_FOLDER, random.choice(images))

# === ОТПРАВКА ФОТО ===
async def post_photo():
    photo_path = get_random_photo()

    if photo_path is None:
        print("Нет фото в папке")
        return

    caption = generate_caption()

    try:
        with open(photo_path, "rb") as photo:
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=photo,
                caption=caption
            )

        print(f"Отправлено: {photo_path}")

        # удаляем только после успешной отправки
        os.remove(photo_path)

    except Exception as e:
        print("Ошибка:", e)

# === ЦИКЛ ===
async def main():
    print("Бот запущен...")

    while True:
        await post_photo()
        print("Ждём 9 часов...")
        await asyncio.sleep(POST_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())