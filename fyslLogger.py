import logging
from pathlib import Path


class fyslLogger:
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.set_up_output_log_file()

    def set_up_output_log_file(self):
        log_file_path = Path(r"./log")
        log_file_path.mkdir(parents=True, exist_ok=True)

        fh = logging.FileHandler(str(log_file_path.joinpath(r"fysl.log")))
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        # add the handlers to self.logger
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
