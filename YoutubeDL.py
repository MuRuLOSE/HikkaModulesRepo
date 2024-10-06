import asyncio
import logging
import yt_dlp
import tempfile
import os

from telethon.types import Message
from .. import loader, utils


"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 

                                   
    YoutubeDL
"""

# scopes:

# 🔒      Licensed under the GNU AGPLv3

# meta banner: https://0x0.st/s/h111E8AonLcGdpV5N8rx6A/XWiz.jpg
# meta desc: Download youtube videos
# meta developer: @BruhHikkaModules

# requires: yt-dlp[default]

logger = logging.getLogger("YoutubeDL")


# It is necessary for auto update of the library, because it is frequently updated
async def update_lib():
    
    process = await asyncio.create_subprocess_shell(
        'pip install -U "yt-dlp[default]""',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    return True
    
async def check_ffmpeg():
    ffmpeg = await asyncio.create_subprocess_shell(
        'ffmpeg',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    ffprobe = await asyncio.create_subprocess_shell(
        'ffprobe',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    status = {
        "ffmpeg": ffmpeg.returncode != 127,
        "ffprobe": ffprobe.returncode != 127
    }

    return status

@loader.tds
class YoutubeDL(loader.Module):
    """Download youtube videos"""

    strings = {
        "name": "YoutubeDL",
        "updated": "Libary updated",
        "downloaded": "Video downloaded!",
        "wait": "Wait...",
        "noargs": "No arguments",
        "addedchannel": "Channel added"
    }

    strings_ru = {
        "_cls_doc": "Скачивайте ютуб ролики",
        "updated": "Библиотека обновлена",
        "downloaded": "Видео скачано!",
        "wait": "Ожидайте...",
        "noargs": "Нет аргументов",
        "addedchannel": "Канал добавлен"
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "channels",
                [],
                "xfdX123L",
                validator=loader.validators.Series()
            ),
            loader.ConfigValue(
                "proxyurl",
                "http://host:port",
                "URL for proxy (http, https, socks5)",
                validator=loader.validators.Hidden()
            ),
            loader.ConfigValue(
                "alwaysproxy",
                False,
                "Use proxy always?",
                validator=loader.validators.Boolean()
            )
        )
        
    async def client_ready(self, client, db):
        status = await check_ffmpeg()
        
        if not status['ffmpeg']:
            logger.info("ffmpeg not installed")
        if not status['ffprobe']:
            logger.info("ffprobe not installed")

        self._common = await self.import_lib(
            "https://raw.githubusercontent.com/MuRuLOSE/HikkaModulesRepo/main/libaries/common.py",
            suspend_on_error=True
        )


        self._utils_chat, _ = await utils.asset_channel(
            self._client,
            "YoutubeDL // Chat",
            "Utils chat for YoutubeDL",
            silent=True,
            archive=True,
            _folder="hikka",
        )

    @loader.loop(autostart=True, interval=60)
    async def loop(self):
        for channel in self.config['channels']:
            with tempfile.TemporaryDirectory() as tempdir:
                ydl_opts = {
                    'outtmpl': os.path.join(tempdir, '%(title)s.%(ext)s'),
                    'download_archive': 'dontremoveyoutubedlarchive.txt',
                    'format': 'best',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(channel)

                downloaded_files = os.listdir(tempdir)

                for file in downloaded_files:
                    full_path = os.path.join(tempdir, file)
                    await self.client.send_file(
                        self._utils_chat,
                        file=full_path,
                        caption=self.strings["downloaded"]
                    )

    @loader.command(
        ru_doc=" - [Ссылка] Скачать видео"
    )
    async def ydownload(self, message: Message):
        """ - [Link] Download video"""
        args_raw = utils.get_args_raw(message)
        args = args_raw.split()

        if args:
            await utils.answer(message, self.strings["wait"])
            
            with tempfile.TemporaryDirectory() as tempdir:
                if "--proxy" in args or self.config["alwaysproxy"]:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(tempdir, '%(title)s.%(ext)s'),
                        'proxy': self.config["proxyurl"]
                    }
                else:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(tempdir, '%(title)s.%(ext)s'),
                    }
                

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([args[0]])

                downloaded_files = os.listdir(tempdir)

                for file in downloaded_files:
                    full_path = os.path.join(tempdir, file)
                    await utils.answer_file(
                        message,
                        full_path,
                        self.strings["downloaded"]
                    )

    @loader.command(
        ru_doc=" - [Channel name (https://www.youtube.com/c/ChannelName/videos)] Add channel to subscriptions"
    )
    async def addchannel(self, message: Message):
        args = utils.get_args_raw(message)
        if args:
            self.config['channels'] = self.config["channels"].append(args)
            await utils.answer(
                message, 
                self.strings["addedchannel"],
                reply_to=await self._common._topic_resolver(message) or None
            )
        else:
            await utils.answer(message, self.strings["noargs"])

    @loader.command(
        ru_doc=" - Обновить библиотеку (если модуль не качает видео)"
    )
    async def yupdate(self, message: Message):
        """ - [Link] Update libary (if module not download viceo)"""
        await update_lib()
        await utils.answer(message, self.strings["updated"])
