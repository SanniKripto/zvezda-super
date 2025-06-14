import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from datetime import datetime, timedelta

TOKEN = '7414197933:AAHJ10jJ7vgW7LSQIwZazM41GBfXeBi1iC4'
CHANNEL_LINK = 'https://t.me/+SicNwm_RIoZlODNk'
SECOND_CHANNEL = 'https://t.me/+SicNwm_RIoZlODNk'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

DATA_FILE = "users.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def get_user(uid):
    data = load_data()
    if str(uid) not in data:
        data[str(uid)] = {
            "stars": 0,
            "invited": [],
            "last_bonus": "2000-01-01"
        }
        save_data(data)
    return data[str(uid)]

def update_user(uid, user_data):
    data = load_data()
    data[str(uid)] = user_data
    save_data(data)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add("📥 Заработать звёзды", "👥 Пригласить друзей")
menu.add("💰 Вывести звёзды", "🏆 Топ участников")
menu.add("🎁 Бонусы", "❓ Как это работает")

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    user = get_user(msg.from_user.id)
    text = f"⭐ Привет, {msg.from_user.first_name}!\n\n" \
           f"Тут ты можешь зарабатывать звёзды и выводить их.\n\n" \
           f"Начинай с кнопок ниже!"
    await msg.answer(text, reply_markup=menu)

    if msg.get_args():
        ref_id = msg.get_args()
        if ref_id != str(msg.from_user.id):
            data = load_data()
            ref_user = data.get(ref_id)
            if ref_user and msg.from_user.id not in ref_user["invited"]:
                ref_user["invited"].append(msg.from_user.id)
                ref_user["stars"] += 25
                update_user(int(ref_id), ref_user)
                await bot.send_message(int(ref_id), f"🎉 Тебе +25 звёзд за друга @{msg.from_user.username or msg.from_user.first_name}")

@dp.message_handler(lambda m: m.text == "📥 Заработать звёзды")
async def earn(msg: types.Message):
    await msg.answer(f"✅ За каждого — +25 звёзд"
                     f"👥 Приглашай друзей по ссылке:\n"
                     f"{CHANNEL_LINK}")

@dp.message_handler(lambda m: m.text == "👥 Пригласить друзей")
async def invite(msg: types.Message):
    user = get_user(msg.from_user.id)
    await msg.answer(f"👥 Ты пригласил: {len(user['invited'])} друзей\n"
                     f"🟡 У тебя: {user['stars']} звёзд\n"
                     f"Твоя ссылка: {CHANNEL_LINK}")

@dp.message_handler(lambda m: m.text == "💰 Вывести звёзды")
async def withdraw(msg: types.Message):
    user = get_user(msg.from_user.id)
    stars = user["stars"]
    invited = len(user["invited"])
    if stars < 1000:
        left = 1000 - stars
        need = max(0, (left + 24) // 25)
        await msg.answer(f"❗ Вывод возможен только от 1000 звёзд\n"
                         f"У тебя: {stars} звёзд\n\n"
                         f"Пригласи ещё {need} друзей, чтобы получить выплату\n"
                         f"💸 Не забудь: вывод возможен только для активных аккаунтов (у которых 40+ друзей).")
    else:
        await msg.answer("🔐 Заявка на вывод отправлена.\n"
                         "💬 Ответ придёт в течение 7 рабочих дней.\n\n"
                         f"👀 Хотите ускорить? Подпишитесь на наш второй канал: {SECOND_CHANNEL}\n"
                         "И пригласите ещё 5 друзей!")

@dp.message_handler(lambda m: m.text == "🏆 Топ участников")
async def top(msg: types.Message):
    data = load_data()
    sorted_users = sorted(data.items(), key=lambda x: x[1]["stars"], reverse=True)[:10]
    text = "🏆 Топ 10 участников:\n\n"
    for i, (uid, udata) in enumerate(sorted_users, 1):
        name = f"@user{uid}"  # заменить по желанию
        text += f"{i}) {name} — {udata['stars']}⭐\n"
    await msg.answer("""🥇 1 место — Эрик Джан
✅ Вывел уже 5 000+ звёзд
✅ Активен каждый день
✅ Рекомендует друзьям
🔥 Настоящий топ! Без лишнего шума — просто делает бабки.
✳️ Уровень доверия: ⭐⭐⭐⭐⭐

🥈 2 место — Zuuulol
✅ Вывел уже 1500+ звёзд
✅ Приглашает людей
✅ Выполняет все условия
⚡ Идёт к вершине уверенно
✳️ Уровень доверия: ⭐⭐⭐⭐

🥉 3 место — mrBeast
✅ Участвует в розыгрышах
✅ Делится ботом с друзьями
✅ Нарабатывает репутацию
📈 Скоро поднимется выше
✳️ Уровень доверия: ⭐⭐⭐

🏅 4 место — MaksQunem
✅ Есть первые выводы
✅ Приглашения пошли
💪 Врывается в таблицу лидеров
✳️ Уровень доверия: ⭐⭐

🎖 5 место — BenjaminFranclin
✅ Только начал, но уже в топе
✅ Проявляет актив
⏳ Всё только начинается
✳️ Уровень доверия: ⭐""")

@dp.message_handler(lambda m: m.text == "🎁 Бонусы")
async def bonus(msg: types.Message):
    user = get_user(msg.from_user.id)
    last = datetime.strptime(user["last_bonus"], "%Y-%m-%d")
    if datetime.now() - last >= timedelta(days=1):
        user["stars"] += 10
        user["last_bonus"] = datetime.now().strftime("%Y-%m-%d")
        update_user(msg.from_user.id, user)
        await msg.answer("🎉 Ты получил +10 звёзд за ежедневный бонус!")
    else:
        await msg.answer("❌ Ты уже получал бонус сегодня. Возвращайся завтра!")

@dp.message_handler(lambda m: m.text == "❓ Как это работает")
async def how(msg: types.Message):
    await msg.answer("📖 Как всё работает:\n\n"
                     "1. Приглашай друзей по ссылке\n"
                     "2. За каждого друга — +25 звёзд\n"
                     "3. Бонусы каждый день — +10 звёзд\n"
                     "4. С 1000 звёзд можно подать заявку на вывод\n\n"
                     f"🧾 Не забудь подписаться на наш канал: {CHANNEL_LINK}")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
