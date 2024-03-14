import os
import logging

config = dict(
    DATABASE_URL=os.getenv("TOUDOU_DATABASE_URL", ""),
    DEBUG=os.getenv("TOUDOU_DEBUG", "False") == "True",
    TOUDOU_FOLDER=os.getenv("TOUDOU_FOLDER", ""),
    FILE_NAME_CSV=os.getenv("FILE_NAME_CSV", "")
)

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s[%(levelname)s] %(message)s",
  handlers=[
    logging.FileHandler("toudou.log"),
    logging.StreamHandler()
  ]
)