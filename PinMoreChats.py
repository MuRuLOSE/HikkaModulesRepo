from hikkatl.types import Message, PeerUser, PeerChat, PeerChannel
import hikkatl.utils as TelethonUtils
from .. import loader, utils

# meta developer: @BruhHikkaModules
@loader.tds
class PinMoreChats(loader.Module):

    async def client_ready(self,db,client):
        self.db = db
        self._chats = self.pointer("chats",[])

    
    strings = {
        "name": "PinMoreChats",
        "_cls_doc": " - Allows you to bookmark more than 5 or 10 chats (WARNING! IT DOES NOT PIN CHATS IN TELEGRAM, IT JUST MAKES A LIST OF YOUR CHATS ANCHORED BY THIS MODULE, REMINDER, USERBOT CAN NO MORE THAN YOU CAN)",
        "added": "<b> <emoji document_id=5197688912457245639>✅</emoji> Added chat <code>{}</code> <code>{}</code> </b>",
        "aleardy_in": "<b> <emoji document_id=5440660757194744323>‼️</emoji> This chat is already in the pinned</b>",
        "aleardy_not_in": "<b> <emoji document_id=5440660757194744323>‼️</emoji> This chat is not in the pinned</b>",
        "deleted": "<b> <emoji document_id=5447644880824181073>⚠️</emoji> Chat removed from pinned</b>",
        "pinned": "<b>Pinned chats:</b>\n\n"
    }
    strings_ru = {
        "_cls_doc": "Позволяет закрепить больше чем 5 или 10 чатов (ПРЕДУПРЕЖДЕНИЕ! ОНО НЕ ЗАКРЕПЛЯЕТ ЧАТЫ В ТЕЛЕГРАММЕ, А ПРОСТО ДЕЛАЕТ СПИСОК ИЗ ВАШИХ ЧАТОВ ЗАКРЕПЛЁННЫМ ЭТИМ МОДУЛЕМ, НАПОМИНАЮ, ЮЗЕРБОТ МОЖЕТ НЕ БОЛЬШЕ ЧЕМ ВЫ<)",
        "added": "<b> <emoji document_id=5197688912457245639>✅</emoji> Добавлен чат <code>{}</code> <code>{}</code> </b>",
        "aleardy_in": "<b> <emoji document_id=5440660757194744323>‼️</emoji> Этот чат уже есть в закрепленных</b>",
        "aleardy_not_in": "<b> <emoji document_id=5440660757194744323>‼️</emoji> Этого чата нет в закрепленных</b>",
        "deleted": "<b> <emoji document_id=5447644880824181073>⚠️</emoji> Чат удалён из закреплённых</b>",
        "pinned": "<b>Закреплённые чаты:</b>\n\n",
    }

    @loader.command(
        ru_doc= " - Добавить чат в закреплённых",
    )
    async def pinchat(self, message: Message):
        """ - Add chat to pinned"""
        peer = TelethonUtils.get_peer(message.peer_id)
        added = "maybe error in code, but i dont care"
        if message.chat_id in self._chats:
            await utils.answer(message,self.strings("aleardy_in"))
            return

        self._chats.append(message.chat_id)
        entity = await self.client.get_entity(message.chat_id)
        if isinstance(peer, PeerUser):
            added = self.strings("added").format(
                message.chat_id,
                entity.first_name
            )
        elif isinstance(peer, PeerChat) or isinstance(peer, PeerChannel):
            added = self.strings("added").format(
                message.chat_id,
                entity.title
            )
        
        await utils.answer(message,added)
    
    @loader.command(
        ru_doc= " - Удалить чат из закреплённых"
    )
    async def unpinchat(self, message):
        ''' - Remove chat from pinned'''

        if message.chat_id not in self._chats:
            await utils.answer(message,self.strings("aleardy_not_in"))
            return
        
        self._chats.remove(message.chat_id)
        await utils.answer(message,self.strings("deleted"))

    @loader.command(
        ru_doc= " - Посмотреть закреплённые чаты"
    )
    async def listpinchats(self,message):
        ''' - View pinned chats'''
        
        name = ""
        chats = ""
        for chat in self._chats:
            peer = TelethonUtils.get_peer(chat)
            chat_id = ""
            try:
                entity = await self.client.get_entity(int(chat))
            except ValueError:
                name = "Чат не найден"
            try:
                chat_id = chat.replace(-100,)
            except Exception:
                pass # просто если нету -100 то и не надо
            try:
                if isinstance(peer, PeerUser):
                    name = entity.first_name
                elif isinstance(peer, PeerChat):
                    name = entity.title
                elif isinstance(peer, PeerChannel):
                    name = entity.title
                else:
                    name = entity.title
            except Exception:
                pass
            messages = await self.client.get_messages(chat_id, limit=1)
            max_message_id = messages[0].id
            chats += f"<a href=tg://privatepost?channel={chat}&post={max_message_id}>{name}</a>\n"
        
        await utils.answer(message,self.strings("pinned") + chats) # Почему через плюс? Потому что f-string ругается SyntaxError: f-string: unmatched '('


    @loader.command(
        ru_doc = " - FAQ по модулю"
    )
    async def pmcfaq(self,message):
        ''' - FAQ for module'''

        
        



