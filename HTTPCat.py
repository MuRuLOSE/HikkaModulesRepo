from hikkatl.types import Message
from .. import loader, utils
import random
from ..inline.types import InlineCall

# meta developer: @BruhHikkaModules


@loader.tds
class HTTPCat(loader.Module):
    """Funny images with HTTP statuses"""

    strings = {
        "name": "HTTPCat",
        "cat": "Here's your {} cat.",
        "update": "Update"
    }
    strings_ru = {
        "cat": "Вот тебе твой {} кот.",
        "update": "Обновить"
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

        reply_markup=[
            [
                {
                    "text": f"🔁 {self.strings['update']}",
                    "callback": self.update
                },

                {
                    "text": "❌ Close",
                    "action": "close"
                }
            ]
        ]
        
        args = utils.get_args_raw(message)

        if not args:
            code = str(random.choice(
                [value for sublist in self.httpstatuses.values() for value in sublist]
            ))

            await self.inline.form(
                text=self.strings["cat"].format(
                    code
                ),
                photo=self.api + code + '.jpg',
                message=message,
                reply_markup=reply_markup
            )

        else:
            await self.inline.form(
                text=self.strings["cat"],
                photo=self.api + str(args) + '.jpg',
                message=message,
                reply_markup=reply_markup
            )

        # why jpg at end? to make sure that telegram sends it correctly.


    async def update(self,call: InlineCall):
        
        reply_markup=[
            [
                {
                    "text": f"🔁 {self.strings['update']}",
                    "callback": self.update
                },

                {
                    "text": "❌ Close",
                    "action": "close"
                }
            ]
        ]
        
        code = str(random.choice(
                [value for sublist in self.httpstatuses.values() for value in sublist]
            ))
        await call.edit(
            photo=self.api + code + '.jpg',
            text=self.strings["cat"].format(
                code
            ),
            reply_markup=reply_markup
        )
