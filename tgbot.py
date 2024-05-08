from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
# izveido bota pieslēgumu Telegram
app = ApplicationBuilder().token("7112507583:AAGIDFfC-NsKjdeX_T1uj0_nOdvlps1oBas").build()

# komanda /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm test bot. Type /hello or /echo")

# komanda /hello
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_user)
    await update.message.reply_text("Hello", update.effective_user.first_name, " ", update.effective_user.last_name)

# komanda /echo
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I hear: " + update.effective_user.first_name + update.message.text)

# savieno čata komandu ar funkciju
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("echo", echo))

# sāk bota darbību
app.run_polling()