# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# '''Если вы хотите взять какую то идею, то упомяните меня в коде, спасибо (но функцию пишите сами)'''

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Not licensed
# meta developer: @bruhHikkaModules 
version = (0,0,10)

from telethon.tl.types import Message, ChatAdminRights
from telethon import functions
import asyncio
from .. import loader, utils
import re
@loader.tds
class PerevodLimitsX(loader.Module): 
    """Модуль для перевода лимитов по новой системе Читайте .faq"""

    strings = {
        "name": "PerevodLimitsX",
        "time_perevod": "Задержка перевода не меньше 1 секунды"
    }

    async def client_ready(self, client, db):
        self._db = db
        self._backup_channel, _ = await utils.asset_channel(
            self._client,
            "LOGS PerevodLimitsX",
            "Группа для логов о переводах модуля PerevodLimitsX Не трогайте!",
            silent=True,
            archive=True,
            _folder="hikka",
        )

        await self.client(functions.channels.InviteToChannelRequest(self._backup_channel, ['@mine_evo_bot']))
        await self.client(functions.channels.EditAdminRequest(
                channel=self._backup_channel,
                user_id="@mine_evo_bot",
                admin_rights=ChatAdminRights(ban_users=True, post_messages=True, edit_messages=True),
                rank="Переводчик",
            )
        )
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "time_perevod",
                2.0,
                lambda: self.strings["time_perevod"],
                validator=loader.validators.Float()
            ),
            loader.ConfigValue(
                "status_perevod",
                False,
                lambda: None,
                validator=loader.validators.Boolean()
            )
        )
    
        
    @loader.command()
    async def perevodx(self,message):
     ''' - [Ник перевода] [Сколько переводить] - Перевод лимитов'''
     self.config["status_perevod"] = True
     args = utils.get_args_split_by(message, " ")
     self.nick = args[0]
     async with self.client.conversation("@mine_evo_bot") as conv:
        await conv.send_message("б")
        await asyncio.sleep(1.5)
        res = await conv.get_response()
        pattern = "<b>Баланс:</b>  (.*?)\n"
        match = re.search(pattern, res.text,re.DOTALL)
        if match:
        	balance = match.group(1)
        self.balance = match.group(1)
        await conv.send_message(f"Перевести {args[0]} {balance}")
        await asyncio.sleep(1.5)
        res = await conv.get_response()
        if "недостаточно денег" in res.text:
        	await utils.answer(message,"⚠️ Откройте конверт (10 в общем пока ошибка не уйдёт)! Я не смог выяснить лимит игрока из-за бага майнево!")
        	return
        pattern = "\n(.*?)$"
        match = re.search(pattern, res.message, re.DOTALL)
        if match:
        	sum = match.group(1).replace("$","")
        self.sum = match.group(1).replace("$","")

        conv.cancel()
        ost = 0
        self.set("full",args[1])
        await utils.answer(message,"💖 Я начал переводить!")
        for i in range(int(args[1])+1):
            
            if self.config["status_perevod"]:
                self._db.get(__name__,"ost",0)
                await self.client.send_message("@mine_evo_bot",f"Перевести {args[0]} {sum}")
                await asyncio.sleep(self.config["time_perevod"])
                ost += 1
                self.set("ost",ost)
            else:
                await utils.answer(message,"🛑 Вы остановили перевод")
                time_1 = self.get("stop_limits_time",10)
                await asyncio.sleep(time_1)
                await utils.answer(message,"Продолжаю перевод")
                self.config["status_perevod"] = True
        await utils.answer(message,"💸 Я всё перевёл")
        await self.client.send_message(self._backup_channel,f"🎉 <b>Я перевел все лимиты игроку:</b> <code>{args[0]}</code> <b>В количстве:</b> <code>{args[1]}</code>")
       	
       	
  
    
    @loader.command()
    async def perevfaq(self,message):
      ''' - FAQ по этому модулю'''
      await utils.answer(message, "Этот модуль предназначен для новой системы перевода лимитов, обновлятся лимиты по мере обновления уровня не будет, потому что в этом и был смысл убирания лимитов.\nРекомендуется запускать не больше одного перевода. Иначе это поломает счетчик")
     
    @loader.command()
    async def limits(self,message):
    	''' - Посмотреть сколько осталось лимитов перевести'''
    	full = self.get("full",0)
    	ost = self.get("ost",0)
    	await utils.answer(message,f"💸 <b>Вы перевели:</b> <code>{ost-1}/{full}</code>")
    
    @loader.command()
    async def time_limits(self,message):
    	''' - Выяснит сколько вам секунд осталось перевести.'''
    	full = self.get("full",0)
    	time = self.config["time_perevod"]
    	ost = self.get("ost",0)
    	r = (int(full)-int(ost)+1)*time
    	await utils.answer(message,f"<b>⏱ Вы будете переводить</b> <code>{r} сек</code>")
    @loader.command()
    async def rs_limits(self,message):
        ''' - [Остановить перевод на время (в секундах)]'''
        args = utils.get_args_raw(message)
        self.config["status_perevod"] = not self.config["status_perevod"]
        msg_status = (
            "✅ Вы продолжили перевод"
            if self.config["status_perevod"]
            else "🛑 Вы остановили перевод"
        )
        await utils.answer(message,msg_status)
        if self.config["status_perevod"]:
            if args != int:
                await utils.answer(message,"Вы указали не число / цифры!")
            elif args == "":
                await utils.answer(message,"Вы указали не число / цифры!")
            else:
                self.set("stop_limits_time",args)
