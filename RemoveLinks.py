from hikkatl.types import Message
from .. import loader, utils

# meta developer: @BruhHikkaModules


@loader.tds
class RemoveLinks(loader.Module):
    """Remove links from your messages"""

    async def client_ready(self, db, client):
        self._rmchats = self.pointer("chats", [])

    strings = {"name": "RemoveLinks", "link_remove": "[HYPERLINK BLOCKED!]"}

    strings_ru = {
        "_cls_doc": "Удаляй ссылки из твоих сообщений",
        "link_remove": "[ГИПЕРССЫЛКА ЗАБЛОКИРОВАНА!]",
    }

    @loader.command(
        ru_doc=" [status] - Включить / выключить блокировку ссылок",
    )
    async def rmlink(self, message: Message):
        """Hello world"""
        await utils.answer(message, self.strings("hello"))

    @loader.command(
        ru_doc=" [id] - Добавить / Удалить чат где блокируется ссылки (если добавить *, удаление будет глобальным во всех чатах)",
    )
    async def addrmlink(self, message: Message):
        """Hello world"""
        await utils.answer(message, self.strings("hello"))
