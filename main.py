import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message = update.message

    info = (
        f"<b>Новое сообщение от клиента</b>\n"
        f"<b>Имя:</b> {user.first_name}\n"
        f"<b>Username:</b> @{user.username if user.username else 'нет'}\n"
        f"<b>User ID:</b> {user.id}\n"
        f"<b>Время:</b> {message.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"<b>Текст:</b> {message.text}"
    )

    await context.bot.send_message(chat_id=GROUP_ID, text=info, parse_mode="HTML")
    await context.bot.send_message(chat_id=ADMIN_ID, text=info, parse_mode="HTML")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))
    app.run_polling()
