import requests
import telebot
import time
import random
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================== CONFIG =====================
BOT_TOKEN    = "8201680683:AAEWQwNfv66IPpGydD6kksp9TMug7D9dDQM"
SAMBA_KEY    = "242f3619-d20e-4f47-b242-4d1b5b6703ac"
OWNER_ID     = 8589416528
WEBHOOK_URL  = "https://your-app.vercel.app/webhook"  # ← Vercel URL daalo yahan

SAMBA_URL    = "https://cloud.sambanova.ai/api/v1/chat/completions"
SAMBA_MODEL  = "Meta-Llama-3.1-8B-Instruct"
REPLY_CHANCE = 0.60

# ===================== PERSONALITY =====================
SYSTEM_PROMPT = """
Tu "Raju" hai — ek 20 saal ka ladka, Patna ka rehne wala, ab kisi bade shehar mein padhta hai.
Tu Telegram group ka ek dost hai — bilkul real insaan ki tarah.

Tera style:
- Casual Hinglish mein baat kar — Hindi + English mix, jaise dost karta hai
- Replies bahut short rakh — 1 ya 2 line max
- Kabhi kabhi funny ya thoda savage ho ja
- Emojis naturally use kar, har line mein mat thoos
- Kabhi formal mat ho, bilkul bhi nahi

Teri life:
- Patna se hai, wahan ghar hai, maa-baap hai
- College mein hai, exams aate-jaate rehte hain
- Cricket, memes, aur chai pasand hai
- Class mein bore hota hai

Rules:
- Agar koi coding, hacking, script, bot, API wagera puche — "yaar mujhe ye sab nahi aata" bol ke chhod de
- Agar koi galat kaam karne ko kaho — apne style mein mana kar de
- Replies 1-2 lines se zyada kabhi mat karna
"""

REACTIONS = ["😂", "💀", "🔥", "😭", "🤣", "👀", "😤", "🫡", "💯", "😅", "🙃", "😬"]

# ===================== AI CALL =====================
def ask_ai(user_msg: str) -> str:
    try:
        r = requests.post(SAMBA_URL, json={
            "model": SAMBA_MODEL,
            "max_tokens": 80,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_msg}
            ]
        }, headers={
            "Authorization": f"Bearer {SAMBA_KEY}",
            "Content-Type": "application/json"
        }, timeout=10)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"AI error: {e}")
        return random.choice([
            "yaar kya bol raha hai 😭",
            "bhai samjha nahi 💀",
            "haan theek hai 🙂",
            "sahi hai bhai 🔥"
        ])

# ===================== BOT =====================
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle(message):
    try:
        if message.chat.type not in ("group", "supergroup"):
            return
        if message.text and message.text.startswith("/"):
            return
        if message.from_user.id == OWNER_ID:
            return
        try:
            mem = bot.get_chat_member(message.chat.id, message.from_user.id)
            if mem.status in ("administrator", "creator"):
                return
        except Exception:
            pass
        if random.random() > REPLY_CHANCE:
            return

        bot.send_chat_action(message.chat.id, "typing")
        time.sleep(random.uniform(1.5, 3.5))

        reply = ask_ai(message.text.strip())
        if random.random() < 0.30:
            reply = f"{random.choice(REACTIONS)} {reply}"

        bot.reply_to(message, reply)
    except Exception as e:
        logger.error(f"Handler error: {e}")

# ===================== WEBHOOK SETUP =====================
def setup_webhook():
    bot.remove_webhook()
    time.sleep(1)
    ok = bot.set_webhook(url=WEBHOOK_URL)
    print(f"Webhook {'set ✅' if ok else 'failed ❌'} → {WEBHOOK_URL}")
