import os
import pandas as pd
from flask import Flask, request
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters

# Environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))
HOST = os.environ.get("HOST", "0.0.0.0")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"https://panditji-bot.onrender.com{WEBHOOK_PATH}"

# Load local NSE/BSE data from CSV file
try:
    stock_data = pd.read_csv("nse_bse_data.csv")
except:
    stock_data = pd.DataFrame()

# Telegram Bot Handlers
def setup_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🙏 जय श्री राम! मैं Panditji Bot हूं। आपका स्वागत है 🕉")

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "🧠 *Panditji Bot Commands*\n"
            "\n"
            "✅ /start - बॉट शुरू करें\n"
            "✅ /help - सभी कमांड्स की लिस्ट\n"
            "✅ /news - आज की महत्वपूर्ण मार्केट न्यूज़\n"
            "✅ /trend <STOCK/INDEX> - मार्केट ट्रेंड बताएं (AI आधारित)\n"
            "✅ /fundamentals <STOCK> - कंपनी के फंडामेंटल्स\n"
            "✅ /oi <STOCK> - ऑप्शन चेन + पीसीआर\n"
            "✅ /scan - स्क्रीनशॉट भेजें, पैटर्न डिटेक्ट करें\n"
            "✅ /pcr <STOCK> - Put/Call Ratio\n"
            "✅ /ratios <STOCK> - सभी financial ratios\n"
            "✅ /livemarket - लाइव मार्केट हाल\n"
            "✅ /details <STOCK> - शेयर की पूरी जानकारी CSV से\n"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    return app

# Flask app
web_app = Flask(__name__)
bot_app = setup_bot()

@web_app.route('/')
def home():
    return "✅ Panditji Bot is running with webhook!"

@web_app.post(WEBHOOK_PATH)
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        bot_app.update_queue.put(update)
        return "", 200

if __name__ == '__main__':
    bot_app.bot.set_webhook(WEBHOOK_URL)
    web_app.run(host=HOST, port=PORT)
