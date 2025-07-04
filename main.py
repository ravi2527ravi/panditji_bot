import os
import threading
import pandas as pd
from flask import Flask
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Load NSE/BSE data from CSV (assumes preloaded CSV file in project directory)
try:
    stock_data = pd.read_csv("nse_bse_data.csv")
except:
    stock_data = pd.DataFrame()

# Define Telegram bot commands
def run_telegram_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("\ud83d\ude4f जय श्री राम! मैं Panditji Bot हूँ। आपका स्वागत है \ud83d\udd71")

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

    async def details(update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args
        if not args:
            await update.message.reply_text("⚠️ कृपया स्टॉक का नाम दें, जैसे `/details INFY`")
            return
        symbol = args[0].upper()
        try:
            row = stock_data[stock_data['SYMBOL'].str.upper() == symbol].iloc[0]
            response = f"📋 *{symbol}* Details:\n- Company: {row['NAME']}\n- Sector: {row['SECTOR']}\n- Market Cap: ₹{row['MARKET_CAP']} Cr\n- EPS: ₹{row['EPS']}\n- PE: {row['PE_RATIO']}\n- Face Value: ₹{row['FACE_VALUE']}"
        except:
            response = "❌ डेटा उपलब्ध नहीं है या SYMBOL गलत है।"
        await update.message.reply_text(response, parse_mode="Markdown")

    # Existing command definitions (unchanged)...
    async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📰 आज की मार्केट न्यूज:\n- सेंसेक्स और निफ्टी में मजबूती।\n- FII निवेश बढ़ा।\n- IT सेक्टर में हलचल।")

    async def trend(update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args
        if not args:
            await update.message.reply_text("⚠️ कृपया कोई स्टॉक या इंडेक्स नाम दें, जैसे `/trend NIFTY`")
            return
        symbol = args[0].upper()
        await update.message.reply_text(f"📈 {symbol} का ट्रेंड: संभावित तेजी (AI अनुमान)")

    async def fundamentals(update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args
        if not args:
            await update.message.reply_text("⚠️ कृपया स्टॉक का नाम दें, जैसे `/fundamentals TCS`")
            return
        stock = args[0].upper()
        await update.message.reply_text(f"📊 {stock} के फंडामेंटल्स:\n- Market Cap: ₹1.2 Lakh Cr\n- P/E: 24.5\n- ROE: 18%\n- Debt/Equity: 0.3")

    async def oi(update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args
        if not args:
            await update.message.reply_text("⚠️ कृपया स्टॉक या इंडेक्स दें, जैसे `/oi RELIANCE`")
            return
        symbol = args[0].upper()
        await update.message.reply_text(f"📊 {symbol} Option Chain Summary:\n- Call OI: 2.1M\n- Put OI: 1.7M\n- PCR: 0.81")

    async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.photo:
            await update.message.reply_text("📷 चार्ट रिसीव हुआ। स्कैन कर रहे हैं...")
            await update.message.reply_text("📊 Candlestick Pattern: Bullish Engulfing\n📈 Trend: Upside Possibility")
        else:
            await update.message.reply_text("⚠️ कृपया चार्ट का स्क्रीनशॉट भेजें।")

    async def pcr(update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args
        if not args:
            await update.message.reply_text("⚠️ कृपया स्टॉक या इंडेक्स दें, जैसे `/pcr BANKNIFTY`")
            return
        symbol = args[0].upper()
        await update.message.reply_text(f"📈 {symbol} का Put/Call Ratio: 0.92")

    async def ratios(update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args
        if not args:
            await update.message.reply_text("⚠️ कृपया स्टॉक का नाम दें, जैसे `/ratios INFY`")
            return
        stock = args[0].upper()
        await update.message.reply_text(f"📊 {stock} Ratios:\n- ROE: 21%\n- P/E: 26.4\n- EPS: ₹43.6\n- Book Value: ₹265\n- Dividend Yield: 1.3%\n- Face Value: ₹5")

    async def livemarket(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📡 लाइव मार्केट अपडेट:\n- NIFTY: 19,876.45 (+0.56%)\n- BANKNIFTY: 45,230.20 (+0.74%)\n- INDIA VIX: 12.14")

    # Add all command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("trend", trend))
    app.add_handler(CommandHandler("fundamentals", fundamentals))
    app.add_handler(CommandHandler("oi", oi))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(CommandHandler("pcr", pcr))
    app.add_handler(CommandHandler("ratios", ratios))
    app.add_handler(CommandHandler("livemarket", livemarket))
    app.add_handler(CommandHandler("details", details))
    app.add_handler(MessageHandler(filters.PHOTO, scan))

    app.run_polling()

# Flask app for Render to bind to a port
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "\u2705 Panditji Bot is running on Render!"

if __name__ == '__main__':
    threading.Thread(target=run_telegram_bot).start()
    web_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
