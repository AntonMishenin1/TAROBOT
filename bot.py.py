import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
# Словарь: user_id → [Аркан1, Аркан2, Аркан3]
user_arcana_map = {}

# Замени на свой Telegram ID
ADMIN_ID = 7213698409  # ← сюда вставь свой ID из @userinfobot
# Список Арканов
ARCANA = [
    "Шут", "Маг", "Жрица", "Императрица", "Император", "Иерофант", "Влюблённые",
    "Колесница", "Справедливость", "Отшельник", "Колесо Фортуны", "Сила", "Повешенный",
    "Смерть", "Умеренность", "Дьявол", "Башня", "Звезда", "Луна", "Солнце", "Суд", "Мир"
]

logging.basicConfig(level=logging.INFO)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔮 Получить предсказание", callback_data="get_fate")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Добро пожаловать в «Судьбу Трёх Арканов»!\n"
        "Нажми кнопку ниже, чтобы получить своё предсказание.",
        reply_markup=reply_markup
    )

# Обработка нажатия на кнопку
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected = random.sample(ARCANA, 3)
    user_id = query.from_user.id
    user_arcana_map[user_id] = selected  # ← сохраняем арканы

    response = (
        f"🧭 Твоя Судьба:\n"
        f"✴️ Прошлое: {selected[0]}\n"
        f"🔁 Настоящее: {selected[1]}\n"
        f"🔮 Будущее: {selected[2]}\n\n"
        f"💬 Напиши историю по выпавшим арканам."
    )

    await query.edit_message_text(text=response)

# Обработка текстовых сообщений от пользователей
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    user_id = user.id

    # Получаем арканы из памяти
    arcana = user_arcana_map.get(user_id)
    arcana_text = (
        f"✴️ Прошлое: {arcana[0]}\n🔁 Настоящее: {arcana[1]}\n🔮 Будущее: {arcana[2]}"
        if arcana else "❗ Арканы не найдены (возможно, кнопку не нажата)"
    )

    # Сообщение тебе в личку
    message = (
        f"📩 Ответ от {user.full_name or user.username} (@{user.username}):\n\n"
        f"{arcana_text}\n\n"
        f"💬 Ответ:\n{text}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=message)

    # Ответ пользователю
    await update.message.reply_text("🔮 Ответ получен. Судьба слушает тебя...")
# Запуск
if __name__ == "__main__":
    BOT_TOKEN = "8158969851:AAEYOJQDd1dsRiaCTdbFfmpf0JuPRZg-NRM"  # ← вставь сюда свой токен от BotFather

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    from telegram.ext import MessageHandler, filters

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Бот запущен.")
    app.run_polling()