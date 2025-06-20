
import os
import logging
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text if update.message else ""
    username = f"@{user.username}" if user.username else "(без username)"
    name = user.full_name
    user_id = user.id

    # Формируем карточку клиента
    text = (
        f"<b>Новое сообщение от клиента</b>

"
        f"<b>Имя:</b> {name}
"
        f"<b>Username:</b> {username}
"
        f"<b>Telegram ID:</b> <code>{user_id}</code>
"
        f"<b>Время:</b> {update.message.date.strftime('%d.%m.%Y %H:%M:%S')}
"
        f"<b>Сообщение:</b> {message}

"
        f'<a href="tg://user?id={user_id}">Ответить клиенту</a>'
    )

    # Отправка владельцу
    await context.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="HTML")

    # Создание топика в группе
    try:
        topic = await context.bot.create_forum_topic(chat_id=GROUP_ID, name=f"{name} | {username or user_id}")
        await context.bot.send_message(chat_id=GROUP_ID, message_thread_id=topic.message_thread_id, text=text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Ошибка при создании топика: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
