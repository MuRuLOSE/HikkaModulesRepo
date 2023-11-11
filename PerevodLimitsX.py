# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# '''Если вы хотите взять какую то идею, то упомяните меня в коде, спасибо (но функцию пишите сами)'''

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Not licensed
# meta developer: @bruhHikkaModules 
version = (0,0,5)

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
        "time_perevod": "Задержка перевода"
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
            )
        )
    
        
    @loader.command()
    async def perevodx(self,message):
        ''' - [Ник перевода] [Сколько переводить] - Перевод лимитов'''
        args = utils.get_args_split_by(message, " ")
        async with self.client.conversation("@mine_evo_bot") as conv:
            await conv.send_message("б")
            res = await conv.get_response()
            pattern = "<b>Баланс:</b>  (.*?)\n"
            match = re.search(pattern, res.text,re.DOTALL)
            if match:
            	balance = match.group(1)
            balance = match.group(1)
            await conv.send_message(f"Перевести {args[0]} {balance}")
            res = await conv.get_response()
            if "недостаточно денег" in res.text:
            	await utils.answer(message,"⚠️ Откройте конверт! Я не смог выяснить лимит игрока из-за бага майнево!")
            	return
            pattern = "\n(.*?)$"
            if match := re.search(pattern, res.message, re.DOTALL):
                sum = match.group(1).replace("$","")

            conv.cancel()
            ost = 0
            self.set("full",args[1])
            await utils.answer(message,"💖 Я начал переводить!")
            for _ in range(int(args[1])+1):
                self._db.get(__name__,"ost",0)
                await self.client.send_message("@mine_evo_bot",f"Перевести {args[0]} {sum}")
                await asyncio.sleep(self.config["time_perevod"])
                ost += 1
                self.set("ost",ost)
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
