from server import Server
from aiogram import Bot, Dispatcher
from settings import Tg

bot = Bot(token=Tg.TOKEN)
dp = Dispatcher(bot)
ids = {}


async def send(server: Server):
    try:
        if server.ip in ids:
            await bot.edit_message_text(text=server.text, chat_id=Tg.CHANNEL_ID, message_id=ids[server.ip])
        else:
            msg = await bot.send_message(Tg.CHANNEL_ID, server.text)
            ids[server.ip] = msg.message_id
    except Exception:
        pass


async def notify(server: Server):
    try:
        await bot.send_message(Tg.ADMIN_ID, server.text)
    except Exception:
        pass