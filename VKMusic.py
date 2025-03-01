from typing import Union, Dict
import aiohttp
from aiohttp.client_exceptions import ServerTimeoutError
import logging
import tempfile
import ffmpeg
from telethon.tl.types import Message
from telethon import types
from .. import loader, utils
from telethon.utils import get_display_name

logger = logging.getLogger(__name__)

class VKMusicAPI:
    def __init__(self, user_id: str, token: str) -> Union[Dict, int]:
        self.token = token
        self.user_id = user_id

    async def get_music(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.vk.com/method/status.get?user_id={self.user_id}&access_token={self.token}&v=5.199"
                ) as response:
                    data: dict = await response.json()
                    if data['response'].get('audio') is not None:
                        return 50, data['response']
                    else:
                        return 40, data['response']['text']
        except ServerTimeoutError:
            return 30

@loader.tds
class VKMusic(loader.Module):
    strings = {
        "name": "VKMusic",
        "no_music": "Music is not playing (not all music is displayed in the status).",
        "server_error": "Server of VK does not answering",
        "music_form": (
            "<emoji document_id=5222175680652917218>🎵</emoji> <b>Listening now:</b> <code>{title}</code>"
            "\n<emoji document_id=5269537556336222550>🐱</emoji> <b>Artist:</b> <code>{artist}</code>"
        ),
        "instructions": (
            "<b>Go to <a href='https://vkhost.github.io/'>vkhost</a>, open settings, leave anytime access and status,"
            "and click get, copy the token and id, and then paste it in properly (in config).</b>"
        ),
        "not_russia": (
            "\n<emoji document_id=5303281542422865331>🇷🇺</emoji> VK gave not all information about" 
            "the track because your userbot server is outside the Russian Federation."
        ),
        "bot_searching": "Searching via Telegram bot...",
        "bot_not_found": "Music not found via Telegram bot.",
        "bot_start": "Bot requires /start, initializing..."
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                "token",
                lambda: "How get token: .vkmtoken",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "user_id",
                "1278631",
                lambda: "Here your userid, (about this in .vkmtoken)",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "telegram_bot",
                "@vkm_bot",
                lambda: "Telegram bot username for music search (e.g., @vkm_bot)",
                validator=loader.validators.String(),
            ),
        )
        self._vkmusic = VKMusicAPI(self.config["user_id"], self.config["token"])

    async def _get_music_from_bot(self, query: str):
        bot_username = self.config["telegram_bot"]
        messages_to_delete = []
        
        async with self.client.conversation(bot_username) as conv:
            request = await conv.send_message(query)
            messages_to_delete.append(request)

            try:
                response = await conv.get_response(timeout=10)
                messages_to_delete.append(response)
            except TimeoutError:
                await conv.send_message("/start")
                messages_to_delete.append(await conv.get_response(timeout=5))
                await conv.send_message(query)
                messages_to_delete.append(await conv.get_response(timeout=10))
                response = messages_to_delete[-1]

            if response.reply_markup and hasattr(response.reply_markup, "rows"):
                music_response = await response.click(0)
                file_response = await conv.get_response(timeout=10)
                messages_to_delete.append(file_response)
            else:
                file_response = response

            if file_response.media and isinstance(file_response.media, types.MessageMediaDocument):
                document = file_response.media.document
                for attr in document.attributes:
                    if isinstance(attr, types.DocumentAttributeAudio):
                        title = attr.title or "Unknown Title"
                        artist = attr.performer or "Unknown Artist"
                        await self.client.delete_messages(bot_username, messages_to_delete)
                        return title, artist, document
                await self.client.delete_messages(bot_username, messages_to_delete)
                return None, None, document
            await self.client.delete_messages(bot_username, messages_to_delete)
            return None, None, None

    @loader.command(ru_doc=" - Текущая песня или поиск через бота")
    async def vkmpnow(self, message: Message):
        args = utils.get_args_raw(message)
        self._vkmusic = VKMusicAPI(str(self.config["user_id"]), str(self.config["token"]))

        music = await self._vkmusic.get_music()

        if music[0] == 50:
            title = music[1]['audio']["title"]
            artist = music[1]['audio']["artist"]
            url = music[1]['audio']["url"]

            with tempfile.TemporaryDirectory() as path:
                input_file = f"{path}/temp.mp3"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        with open(input_file, "wb") as f:
                            f.write(await resp.read())
                await utils.answer_file(
                    message,
                    file=input_file,
                    caption=self.strings["music_form"].format(title=title, artist=artist)
                )
        elif music[0] == 40 or music[0] == 30:
            await utils.answer(message, self.strings["bot_searching"])
            query = args if args else music[1] if music[0] == 40 else "current song"
            title, artist, document = await self._get_music_from_bot(query)

            if document:
                await utils.answer_file(
                    message,
                    file=document,
                    caption=self.strings["music_form"].format(
                        title=title or "Unknown",
                        artist=artist or "Unknown"
                    )
                )
            else:
                await utils.answer(message, self.strings["bot_not_found"])
        elif music == 20:
            await utils.answer(message, self.strings["no_music"])
        elif music == 30:
            await utils.answer(message, self.strings["server_error"])

    @loader.command(ru_doc=" - Инструкции для токена и пользовательского идентификатора")
    async def vkmtoken(self, message: Message):
        await utils.answer(message, self.strings["instructions"])