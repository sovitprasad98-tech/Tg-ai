import requests
import telebot
import time
import random
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================== CONFIG =====================
BOT_TOKEN   = "8600723357:AAHsQYZmRdY8_yfnt2uKQZPMgctFcUuX8OI"
SAMBA_KEY   = "242f3619-d20e-4f47-b242-4d1b5b6703ac"
OWNER_ID    = 8589416528
WEBHOOK_URL = "https://tg-ai-9tpp.vercel.app/webhook"

SAMBA_URL   = "https://api.sambanova.ai/v1/chat/completions"
SAMBA_MODEL = "Meta-Llama-3.1-8B-Instruct"

REACTIONS = ["🔥", "😂", "💀", "❤", "😎", "⚡", "🤣", "👀", "🥶"]

SYSTEM_PROMPT = """
You are a real human friend chatting naturally in Hinglish.
Rules:
- Never say you are AI or bot.
- If someone says you are AI then deny naturally.
- If someone asks coding, scripts, hacking, api, bot, programming then refuse casually.
- Home city is Patna.
- Talk casually like Telegram friends.
- Use short replies only (1-2 lines max).
- Funny sometimes.
- Natural Hinglish only.
- Never formal.
"""

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except:
        return False

def generate_reply(username, message):
    try:
        r = requests.post(SAMBA_URL, json={
            "model": SAMBA_MODEL,
            "temperature": 0.9,
            "top_p": 0.9,
            "max_tokens": 80,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"User: {username}\nMessage: {message}\nReply:"}
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
            "Abe kya bol raha 😂",
            "Bakchodi mat kar 😭",
            "Sahi hai bhai",
            "Patna me bhi aisa hota hai 😂",
            "Are bhai chill"
        ])

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle(message):
    try:
        if message.chat.type not in ("group", "supergroup"):
            return
        if message.text.startswith("/"):
            return
        if message.from_user.id == OWNER_ID:
            return
        if is_admin(message.chat.id, message.from_user.id):
            return

        chat_id  = message.chat.id
        username = message.from_user.first_name or message.from_user.username or "User"

        try:
            bot.set_message_reaction(
                chat_id, message.message_id,
                [telebot.types.ReactionTypeEmoji(random.choice(REACTIONS))]
            )
        except:
            pass

        bot.send_chat_action(chat_id, "typing")
        time.sleep(random.uniform(1.5, 4.5))

        reply = generate_reply(username, message.text.strip())
        bot.reply_to(message, reply)

    except Exception as e:
        logger.error(f"Handler error: {e}")

def setup_webhook():
    bot.remove_webhook()
    time.sleep(1)
    ok = bot.set_webhook(url=WEBHOOK_URL)
    print(f"Webhook {'set ✅' if ok else 'failed ❌'} → {WEBHOOK_URL}")

def startup_log():
    me = bot.get_me()
    print(f"✅ {me.first_name} (@{me.username}) — Online | Patna 🏠")
