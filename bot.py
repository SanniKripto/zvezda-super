from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import json
import os

# Загружаем данные пользователей
DATA_FILE = "users.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    if user_id not in users:
        users[user_id] = {"stars": 0}
        save_users()

    keyboard = [[InlineKeyboardButton("⭐ Получить звёзды", callback_data="get_stars")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Добро пожаловать в ZvezdaTrade бот!", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = str(query.from_user.id)
    query.answer()

    if query.data == "get_stars":
        users[user_id]["stars"] += 1
        save_users()
        query.edit_message_text(text=f"⭐ У тебя теперь {users[user_id]['stars']} звёзд!")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()