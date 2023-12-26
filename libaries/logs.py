from .. import loader
import random
import logging


class LogHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        send_log(record)

class BHikkamodsLogsLib(loader.Library):
    developer = "@MuRuLOSE"


    def __init__(self):
        self.config = loader.LibraryConfig(
            loader.ConfigValue(
                "send_errors",
                False,
                "Send errors to developer for diagnostic",
                validator=loader.validators.String(),
            )
        )
        
        self._log_handler = LogHandler()