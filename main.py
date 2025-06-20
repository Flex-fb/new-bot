import os
import logging
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Ответить", url=f"https://t.me/{user.username}" if user.username else "")]
    ])

    message = (
        f"<b>Новое сообщение от клиента</b>\n\n"
        f"<b>Имя:</b> {user.first_name}\n"
        f"<b>Username:</b> @{user.username if user.username else '—'}\n"
        f"<b>ID:</b> <code>{user.id}</code>\n"
        f"<b>Время:</b> <code>{update.message.date}</code>\n"
        f"<b>Текст:</b> {text}"
    )

    await context.bot.send_message(chat_id=GROUP_ID, text=message, parse_mode="HTML", reply_markup=keyboard)
    await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="HTML")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
