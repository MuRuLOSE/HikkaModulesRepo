from hikkatl.types import Message
from .. import loader, utils
from telethon.tl.types import MessageService
import asyncio
# meta developer: @BruhHikkaModules

@loader.tds
class ControlSpam(loader.Module):
    """Не просто спамь, а контролируй"""
    strings = {"name": "ControlSpam", "hello": "Hello world!"}
    strings_ru = {"hello": "Привет мир!"}

    

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                True,
                lambda: "Просто статус спама",
                validator=loader.validators.Boolean()
            )
        ) 
    @loader.command()
    async def spam(self, message: Message):
        """ [количество спама] [текст / реплай]  - Начать спам"""
        self.config["status"] = True
        args = utils.get_args(message)
        a = 0
        reply = await message.get_reply_message()
        text = "Something get wrong"
        type_topic = False
        topic_id = None
        if reply:
            if isinstance(reply, MessageService):
                text = " ".join(args[1:])
                type_topic = True
                topic_id = message.reply_to_msg_id
            else:
                text = reply.text
        else:
            text = " ".join(args[1:])
        await utils.answer(message,"Я начал спамить")
        while self.config["status"]:
            
            if a == int(args[0]):
                break
            a += 1
            
            if type_topic:
                await self.client.send_message(message.chat_id,text,reply_to=topic_id)
            else:
                await self.client.send_message(message.chat_id,text)

        

    @loader.command()
    async def delayspam(self, message: Message):
        """ [количество спама] [Задержка в секундах] [текст / реплай]  - Начать спам"""
        self.config["status"] = True
        args = utils.get_args(message)
        a = 0
        reply = await message.get_reply_message()
        text = "Something get wrong"
        type_topic = False
        topic_id = None
        if reply:
            if isinstance(reply, MessageService):
                text = " ".join(args[2:])
                type_topic = True
                topic_id = message.reply_to_msg_id
            else:
                text = reply.text
        else:
            text = " ".join(args[2:])
        await utils.answer(message,"Я начал спамить")
        while self.config["status"]:
            
            if a == int(args[0]):
                break
            a += 1
            if type_topic:
                await self.client.send_message(message.chat_id,text,reply_to=topic_id)
            else:
                await self.client.send_message(message.chat_id,text)
            await asyncio.sleep(int(args[1]))

        
            
    
    @loader.command()
    async def spam_stop(self, message: Message):
        ''' - Закончить весь спам'''
        self.config["status"] = False
        await utils.answer(message,"Я закончил спамить")

    
