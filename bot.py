
import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = 9286725831:AAEAwI2CjrqjAsw-lfwdeZmcOAdOz3dNhTQ

games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    games[chat_id] = {"number": random.randint(1, 100), "tries": 0}
    await context.bot.send_message(
        chat_id=chat_id,
        text="🎲 Я загадал число от 1 до 100.\nПиши число в чат!"
    )

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in games:
        await update.message.reply_text("Нажми /start, чтобы начать.")
        return
    try:
        user_num = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Это не число 🤔")
        return
    game = games[chat_id]
    game["tries"] += 1
    target = game["number"]
    if user_num < target:
        await update.message.reply_text(f"📈 Больше! (попытка {game['tries']})")
    elif user_num > target:
        await update.message.reply_text(f"📉 Меньше! (попытка {game['tries']})")
    else:
        await update.message.reply_text(
            f"🎉 Угадал! Число {target}. Попыток: {game['tries']}.\nЕщё раз — /start"
        )
        del games[chat_id]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), guess))
    print("Бот запущен...")
    app.run_polling()
