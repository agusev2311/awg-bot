import logging
from rich.logging import RichHandler
import datetime
import os

# logs
def setup_logging():
    os.makedirs(".logs", exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        f".logs/{datetime.datetime.now(datetime.timezone.utc)}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d) | %(message)s")
    )
    
    console_handler = RichHandler(
        show_time=True,
        show_path=True,
        rich_tracebacks=True,
    )
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)