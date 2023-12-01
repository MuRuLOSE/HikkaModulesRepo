from hikkatl.types import Message
from .. import loader, utils
import random

# meta developer: @BruhHikkaModules


@loader.tds
class HTTPCat(loader.Module):
    """Funny images with HTTP statuses"""

    strings = {
        "name": "HTTPCat",
        "cat": "Here's your {} cat."
    }
    strings_ru = {
        "cat": "Вот тебе твой {} кот."
    }

    def __init__(self):
        self.api = "https://http.cat/"
        self.httpstatuses = {
            "1xx": [
                100, 101, 102,
                103
            ],

            "2xx": [
                200, 201, 202,
                203, 204, 205,
                206, 207, 208,
                226,
            ],

            "3xx": [
                300, 301, 302,
                303, 304, 305,
                306, 307, 308,
            ],

            "4xx": [
                400, 401, 402,
                403, 404, 405,
                406, 407, 408,
                409, 410, 411,
                412, 413, 414,
                415, 416, 417,
                418, 421, 422,
                423, 424, 425,
                426, 428, 429,
                431, 451
            ],

            "5xx": [
                500, 501, 502,
                503, 504, 505,
                506, 507, 508,
                510, 511
            ]
        }

    @loader.command(
        ru_doc=" [HTTP Статус / Ничего] - Получить картинку с котом и HTTP кодом",
    )
    async def gethttpcat(self, message: Message):
        """ [HTTP Status / Nothing] - Get picture with cat and HTTP code"""
        
        args = utils.get_args_raw(message)

        if not args:
            code = str(random.choice(
                [value for sublist in self.httpstatuses.values() for value in sublist]
            ))
            await utils.answer_file(
                message,
                self.api + code + '.jpg',
                caption=self.strings["cat"].format(
                    code
                ),
                force_document=False
            )

        else:
            await utils.answer_file(
                message,
                self.api + str(args) + '.jpg',
                caption=self.strings["cat"].format(
                    str(args)
                ),
                force_document=False
            )

        # why jpg at end? to make sure that telegram sends it correctly.

