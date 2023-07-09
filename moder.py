from pyrogram import Client, types
from .. import loader, utils


@loader.module(name="Moderation",dev="Murls",version=(0,1,0))
class ModerationMod(loader.Module):
    """Модуль для модерации беседы"""


    async def kick_cmd(self, app: Client, message: types.Message, args: str):
        """Команда для исключения пользователя из беседы. Использование: kick [юзернейм или ID]"""
        chat = message.chat
        if args:
            user = await app.get_users(args)
            if user:
                await app.kick_chat_member(chat.id, user.id)
                await utils.answer(message, f"Пользователь {user.first_name} был исключен из беседы")
            else:
                await utils.answer(message, f"Пользователь {args} не найден")
        else:
            await utils.answer(message, "Укажите юзернейм или ID пользователя")


    async def ban_cmd(self, app: Client, message: types.Message, args: str):
        """Команда для блокировки пользователя в беседе. Использование: ban [юзернейм или ID]"""
        chat = message.chat
        if args:
            user = await app.get_users(args)
            if user:
                await app.kick_chat_member(chat.id, user.id, revoke=True)
                await utils.answer(message, f"Пользователь {user.first_name} был заблокирован в беседе")
            else:
                await utils.answer(message, f"Пользователь {args} не найден")
        else:
            await utils.answer(message, "Укажите юзернейм или ID пользователя")