from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8249452727:AAExS5DziVnWEUy2kXO-pwFZ5nmhiCt2aBs"

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    
    await update.message.reply_text(f"Você disse: {texto}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, responder))

app.run_polling()

