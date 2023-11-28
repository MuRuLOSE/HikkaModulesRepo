from hikkatl.types import Message
from .. import loader, utils

__version__ = (3.14, 16, 18)


# meta developer: @BruhHikkaModules
@loader.tds
class Morse(loader.Module):
    """- Decode and Encode morse code"""

    strings = {"name": "Morse"}
    strings_ru = {"_cls_doc": " - Зашифровывает и расшифровывает азбуку морзе"}

    @loader.command(ru_doc=" - [Текст] - Переводит в азбуку морзе")
    async def decode_morse(self, message: Message):
        """- [Text] - Translates into morse code"""
        args = utils.get_args_raw(message)
        morse_code = {
            "A": ".-",
            "B": "-...",
            "C": "-.-.",
            "D": "-..",
            "E": ".",
            "F": "..-.",
            "G": "--.",
            "H": "....",
            "I": "..",
            "J": ".---",
            "K": "-.-",
            "L": ".-..",
            "M": "--",
            "N": "-.",
            "O": "---",
            "P": ".--.",
            "Q": "--.-",
            "R": ".-.",
            "S": "...",
            "T": "-",
            "U": "..-",
            "V": "...-",
            "W": ".--",
            "X": "-..-",
            "Y": "-.--",
            "Z": "--..",
            "А": ".-",
            "Б": "-...",
            "В": ".--",
            "Г": "--.",
            "Д": "-..",
            "Е": ".",
            "Ж": "...-",
            "З": "--..",
            "И": "..",
            "Й": ".---",
            "К": "-.-",
            "Л": ".-..",
            "М": "--",
            "Н": "-.",
            "О": "---",
            "П": ".--.",
            "Р": ".-.",
            "С": "...",
            "Т": "-",
            "У": "..-",
            "Ф": "..-.",
            "Х": "....",
            "Ц": "-.-.",
            "Ч": "---.",
            "Ш": "----",
            "Щ": "--.-",
            "Ъ": "--.--",
            "Ы": "-.--",
            "Ь": "-..-",
            "Э": "..-..",
            "Ю": "..--",
            "Я": ".-.-",
        }
        text = args.upper()
        result = []
        for char in text:
            if char in morse_code:
                result.append(morse_code[char])
            else:
                result.append(char)
        await utils.answer(message, " ".join(result))

    @loader.command(ru_doc=" - [Текст] - Переводит из азбуки морзе в текст")
    async def encode_morse(self, message):
        """- [Text] - Translates from morse code"""
        args = utils.get_args_raw(message)
        morse_code = {
            ".-": "A",
            "-...": "B",
            "-.-.": "C",
            "-..": "D",
            ".": "E",
            "..-.": "F",
            "--.": "G",
            "....": "H",
            "..": "I",
            ".---": "J",
            "-.-": "K",
            ".-..": "L",
            "--": "M",
            "-.": "N",
            "---": "O",
            ".--.": "P",
            "--.-": "Q",
            ".-.": "R",
            "...": "S",
            "-": "T",
            "..-": "U",
            "...-": "V",
            ".--": "W",
            "-..-": "X",
            "-.--": "Y",
            "--..": "Z",
            " ": " ",
            ".-": "А",
            "-...": "Б",
            ".--": "В",
            "--.": "Г",
            "-..": "Д",
            ".": "Е",
            "...-": "Ж",
            "--..": "З",
            "..": "И",
            ".---": "Й",
            "-.-": "К",
            ".-..": "Л",
            "--": "М",
            "-.": "Н",
            "---": "О",
            ".--.": "П",
            ".-.": "Р",
            "...": "С",
            "-": "Т",
            "..-": "У",
            "..-.": "Ф",
            "....": "Х",
            "-.-.": "Ц",
            "---.": "Ч",
            "----": "Ш",
            "--.-": "Щ",
            "--.--": "Ъ",
            "-.--": "Ы",
            "-..-": "Ь",
            "..-..": "Э",
            "..--": "Ю",
            ".-.-": "Я",
        }

        morse_chars = args.split(" ")
        result = []

        for morse_char in morse_chars:
            if morse_char in morse_code:
                result.append(morse_code[morse_char])
            else:
                result.append(morse_char)

        await utils.answer(message, "".join(result))
