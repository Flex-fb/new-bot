import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram.helpers import mention_html

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Константы
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Обработчик новых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message
    first_message = message.text or "<нет текста>"
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    topic_name = f"{user.first_name} | @{user.username}" if user.username else user.first_name

    forum_topic = await context.bot.create_forum_topic(
        chat_id=GROUP_ID,
        name=topic_name
    )
    topic_id = forum_topic.message_thread_id

    text = (
        f"<b>💌 Новое сообщение от клиента</b>

"
        f"<b>Имя:</b> {user.first_name}
"
        f"<b>Username:</b> @{user.username or '—'}
"
        f"<b>ID:</b> <code>{user.id}</code>
"
        f"<b>Дата:</b> {now}
"
        f"<b>Сообщение:</b> {first_message}"
    )

    reply_button = InlineKeyboardMarkup([[
        InlineKeyboardButton("✉️ Ответить", url=f"https://t.me/{user.username}") if user.username else InlineKeyboardButton("Профиль", callback_data="noop")
    ]])

    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=text,
        parse_mode="HTML",
        message_thread_id=topic_id,
        reply_markup=reply_button
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        parse_mode="HTML",
        reply_markup=reply_button
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
