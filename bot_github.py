from pathlib import Path
import os
import json
import random
import asyncio
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PHOTO_FOLDER = Path(".")
STATE_FILE = Path("state.json")

print("BOT_TOKEN exists:", BOT_TOKEN is not None)
print("CHAT_ID exists:", CHAT_ID is not None)
print("BOT_TOKEN length:", len(BOT_TOKEN) if BOT_TOKEN else 0)

bot = Bot(token=BOT_TOKEN)

RUS_CAPTIONS = [
    "Просто обычный момент.",
    "Спокойное настроение на сегодня.",
    "Без лишнего, просто фото.",
    "Обычный кадр из дня.",
    "Просто сохранил этот момент."
]

KZ_CAPTIONS = [
    "Жай ғана бір сәт.",
    "Бүгінгі көңіл күй тыныш.",
    "Артық ештеңе жоқ.",
    "Кәдімгі бір көрініс.",
    "Осы сәт есте қалсын."
]

def generate_caption() -> str:
    lang = random.choices(["ru", "kz"], weights=[85, 15], k=1)[0]
    return random.choice(RUS_CAPTIONS if lang == "ru" else KZ_CAPTIONS)

def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"posted": []}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"posted": []}

def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def get_next_photo() -> str | None:
    if not PHOTO_FOLDER.exists():
        return None

    state = load_state()
    posted = set(state.get("posted", []))

    images = [
        str(p) for p in sorted(PHOTO_FOLDER.iterdir())
        if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
    ]

    for img in images:
        if img not in posted:
            return img

    return None

async def main() -> None:
    photo_path = get_next_photo()

    if not photo_path:
        print("Нет новых фото для отправки.")
        return

    caption = generate_caption()

    with open(photo_path, "rb") as photo:
        await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=caption)

    print(f"Отправлено: {photo_path}")

    state = load_state()
    state.setdefault("posted", []).append(photo_path)
    save_state(state)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
