import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])
GROUP_ID = int(os.environ["GROUP_ID"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if user is None or text is None:
        return

    name = user.first_name or ""
    username = user.username or "неизвестно"
    user_id = user.id
    date = update.message.date.strftime("%Y-%m-%d %H:%M:%S")

    message = (
        "<b>💬 Новое сообщение от клиента</b>\n\n"
        f"<b>Имя:</b> {name}\n"
        f"<b>Username:</b> @{username}\n"
        f"<b>Telegram ID:</b> <code>{user_id}</code>\n"
        f"<b>Время:</b> {date}\n"
        f"<b>Сообщение:</b> {text}"
    )

    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Ошибка отправки админу: {e}")

    await update.message.reply_text("Привет, сладкий, хочешь расслабиться и получать незабываемые удовольствия?")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
    app.run_polling()
