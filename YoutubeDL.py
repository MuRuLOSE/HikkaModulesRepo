import asyncio
import logging
import tempfile
import os

from telethon.types import Message
from .. import loader, utils

from pytubefix import YouTube
from pytubefix.exceptions import BotDetection


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

# requires: pytubefix

logger = logging.getLogger("YoutubeDL-BETA")
__version__ = (1, 0, 4)


# It is necessary for auto update of the library, because it is frequently updated (for now, deprecated, not needed)
# async def update_lib():

#     process = await asyncio.create_subprocess_shell(
#         'pip install -U "pafy""',
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE
#     )

#     return True


# async def check_ffmpeg():
#     ffmpeg = await asyncio.create_subprocess_shell(
#         'ffmpeg',
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE
#     )

#     ffprobe = await asyncio.create_subprocess_shell(
#         'ffprobe',
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE
#     )

#     status = {
#         "ffmpeg": ffmpeg.returncode != 127,
#         "ffprobe": ffprobe.returncode != 127
#     }

#     return status


@loader.tds
class YoutubeDLB(loader.Module):
    """THIS IS A BETA! BUGS MAY OCCUR!"""

    strings = {"name": "YoutubeDLB"}

    # todo: token support (PoToken)
    # auto generator, manually

    @loader.command()
    async def videodl(self, message: Message):
        """[link] - Download video"""
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(
                message,
                "no arguments, use this link for example: https://www.youtube.com/watch?v=RM4Ue8Xy55c",
            )

        else:
            youtube = YouTube(args)

            with tempfile.TemporaryDirectory() as path:
                stream = await utils.run_sync(youtube.streams.get_highest_resolution())

                try:
                    await utils.run_sync(stream.download(path, "/video.mp4"))
                except BotDetection:
                    await utils.answer(
                        message,
                        "Youtube recognize in you bot, so, try use PoToken (not ready, so nevermind)",
                    )

                await utils.answer_file(message, path + "/video.mp4")
