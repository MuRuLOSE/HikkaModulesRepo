from hikkatl.types import Message
from .. import loader, utils
import asyncio


@loader.tds
class timer(loader.Module):
    """Модуль который запускает таймер до события"""

    strings = {"name": "timer"}

    @loader.command()
    async def start_timer(self, message: Message):
        """[Таймер на секунды] [Текст напоминания] - Запустить таймер (Сообщения будет отправляться инлайн ботом с вашим упоминанием)"""
        args = utils.get_args_raw(message)

        msg = " ".join(args.split()[1:])
        time = int(args.split(" ", 2)[0])
        await utils.answer(message, "Таймер поставлен")
        await asyncio.sleep(time)
        for _ in range(10):
            me = await self.client.get_me()
            await self.inline.bot.send_message(self.tg_id, f"@{me.username} {msg}")
