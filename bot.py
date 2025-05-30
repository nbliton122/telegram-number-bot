from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

def format_numbers(text, mode):
    lines = text.strip().split('\n')
    formatted = []
    for line in lines:
        num = line.strip().replace('+', '').replace('https://t.me/+', '')
        if mode == 'link':
            formatted.append(f'https://t.me/+{num}')
        elif mode == 'plus':
            formatted.append(f'+{num}')
        elif mode == 'clean':
            formatted.append(num)
    return '\n'.join(formatted)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Use /link, /plus or /clean followed by numbers.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith('/link'):
        raw = text.replace('/link', '')
        output = format_numbers(raw, 'link')
    elif text.startswith('/plus'):
        raw = text.replace('/plus', '')
        output = format_numbers(raw, 'plus')
    elif text.startswith('/clean'):
        raw = text.replace('/clean', '')
        output = format_numbers(raw, 'clean')
    else:
        output = "❗ Use /link, /plus, or /clean followed by numbers."
    await update.message.reply_text(output)

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
