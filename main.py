import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# टेलीग्राम बॉट टोकन को env से लो
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Telegram Bot का function
def run_telegram_bot():
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        # /start कमांड का जवाब
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🙏 जय श्री राम!\nमैं Panditji Bot हूँ 📿\nआपका स्वागत है 🗱\nMarket ka pura analysis yahan milega!"
            )

        # कमांड handler जोड़ें
        app.add_handler(CommandHandler("start", start))

        print("🤖 Telegram bot started...")
        app.run_polling()

    except Exception as e:
        print(f"❌ Telegram bot error: {e}")

# Flask app (Render को port bind दिखाने के लिए)
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "✅ Panditji Bot Flask server is running on Render!"

# Start both Flask + Telegram Bot
if __name__ == '__main__':
    threading.Thread(target=run_telegram_bot).start()
    web_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
