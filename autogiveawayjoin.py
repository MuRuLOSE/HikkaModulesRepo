from hikkatl.types import Message
from .. import loader, utils

import asyncio
import random

# meta developer: @BruhHikkaModules


@loader.tds
class AutoGiveawayJoin(loader.Module):
    """Авто присоеденение к розыгрышам в @mine_evo_bot"""
    strings = {"name": "AutoGiveawayJoin"}

    def __init__(self):
        self.bot = 5522271758
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "join",
                False,
                "Присоеденяться к розыгрышам?",
                validator=loader.validators.Boolean()
            )
        )

    @loader.watcher(from_id=5522271758)
    async def join_giveaway(self, message: Message):

        if message.text == "Success start!" and self.config["join"]:
            await asyncio.sleep(random.randint(2, 5))
            await self.client.send_message(self.bot, "Участвую")

    @loader.command()
    async def giveawayjoin(self, message: Message):
        """ - Вкл / Выкл присоеденение к розыгрышам"""
        self.config["join"] = not self.config["join"]

        status = (
            "Авто присоеденение включено"
            if self.config["join"]
            else "Авто присоеденение выключено"
        )

        await utils.answer(message, status)
