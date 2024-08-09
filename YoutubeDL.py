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

# requires: yd-dlp[default]

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
        "wait": "Ожидайте"
    }
    strings_ru = {
        "_cls_doc": "Скачивайте ютуб ролики",
        "updated": "Библиотека обновлена",
        "downloaded": "Видео скачено!",
        "wait": "Ожидайте..."
    }
        
    async def client_ready(self, client, db):
        status = await check_ffmpeg()
        
        if not status['ffmpeg']:
            logger.info("ffmpeg not installed")
        if not status['ffprobe']:
            logger.info("ffprobe not installed")

    @loader.command(
        ru_doc=" - [Ссылка] Скачать видео"
    )
    async def ydownload(self, message: Message):
        """ - [Link] Download video"""
        args = utils.get_args_raw(message)

        if args:
            await utils.answer(message, self.strings["wait"])
            
            with tempfile.TemporaryDirectory() as tempdir:

                ydl_opts = {
                    'format': 'best',
                    'outtmpl': os.path.join(tempdir, '%(title)s.%(ext)s')
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([args])

                downloaded_files = os.listdir(tempdir)

                for file in downloaded_files:
                    full_path = os.path.join(tempdir, file)
                    await utils.answer_file(
                        message,
                        full_path,
                        self.strings["downloaded"]
                    )

    @loader.command(
        ru_doc=" - Обновить библиотеку (если модуль не качает видео)"
    )
    async def yupdate(self, message: Message):
        """ - [Link] Update libary (if module not download viceo)"""
        await update_lib()
        await utils.answer(message, self.strings["updated"])
