"""
Main runner file.

(C) 2023 - B1ue-Dev
"""

import sys
sys.path.append("src")

import asyncio
import logging
from bot import start
from utils.utils import get_local_time


logger = logging.getLogger()
logging.Formatter.converter = lambda *args: get_local_time().timetuple()
logging.basicConfig(
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level=logging.INFO,
)


if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logger.info("Shutting down.")
