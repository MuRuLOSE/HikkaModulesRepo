from telethon.tl.types import Message
from .. import loader,utils

# meta developer <b>@BruhHikkaModules @evolut</b> 

@loader.tds
class Autoreader(loader.Module):
    """Для автоматического читания в чатах и лс"""
    strings = {"name": "Autoreader"}

    async def client_ready(self,client,db):
        self.db = db
        self._chats = self.pointer("chats",[])
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "read_new_msg_new_users",
                False,
                "Читать сообщения от новых пользователей по-улмолчанию пока не работает :(",
                validator=loader.validators.Boolean()
            )
        )
    
    @loader.watcher()
    async def watcher(self,message):
        if str(message.chat_id) in self._chats:
            message_id = message.id
            await self.client.send_read_acknowledge(message.chat_id,clear_mentions=True)

    @loader.command()
    async def autoread(self, message: Message):
        """ - Добавить / Удалить чат из авто читаемых"""
        added = None
        removed = None
        if message.chat_id not in self._chats:
            self._chats.append(message.chat_id)
            added = True
        elif message.chat_id in self._chats:
            self._chats.remove(message.chat_id)
            removed = True
        if added:
            await utils.answer(message,"Чат добавлен в авто читаемые")
        elif removed:
            await utils.answer(message,"Чат удалён из авто читаемых")
    @loader.command()
    async def list_autoread(self,message):
        ''' - Чаты которые читаются'''
        chats_wha = self.get("chats",[])
        r = str(chats_wha).replace("[","")
        m = r.replace("]","")
        ov = m.replace(" ","")
        hg = ov.replace(",","\n")
        chats = f"👁 <b>Авто просматриваемые чаты:</b>\n{hg}"
        await utils.answer(message,chats)
