import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    first_name = user.first_name or "Неизвестно"
    username = f"@{user.username}" if user.username else "Нет никнейма"
    user_id = user.id
    message_time = update.message.date.strftime("%Y-%m-%d %H:%M:%S")
    profile_link = f"<a href='tg://user?id={user_id}'>Профиль</a>"

    message = (
        "<b>Новое сообщение от клиента</b>"

"
        f"👤 Имя: {first_name}
"
        f"🔗 Никнейм: {username}
"
        f"🆔 Telegram ID: <code>{user_id}</code>
"
        f"🕓 Время: {message_time}
"
        f"💬 Сообщение: {text}
"
        f"{profile_link}"
    )

    await context.bot.send_message(chat_id=GROUP_ID, text=message, parse_mode="HTML")
    await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="HTML")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
