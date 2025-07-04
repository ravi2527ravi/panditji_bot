# Main logic of PanditjiBot
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # 🧠 ye Render mai environment variable se lena hai

# Telegram Bot
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🙏 Jai Shri Ram! Panditji Bot is active 🔱")

    app.add_handler(CommandHandler("start", start))
    app.run_polling()

# Flask App (for Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Panditji Bot Flask App is Live!"

# Run both Flask + Bot
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))   # 🧠 Important for Render
    app.run(host='0.0.0.0', port=port)
