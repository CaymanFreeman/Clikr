import logging


class LogHandler:

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("session.log"),
                logging.StreamHandler(),
            ],
        )
