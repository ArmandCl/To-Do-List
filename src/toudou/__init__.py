import os
config = dict(
DATABASE_URL=os.getenv("TOUDOU_DATABASE_URL", ""),
DEBUG=os.getenv("TOUDOU_DEBUG", "False") == "True",
TOUDOU_FOLDER=os.getenv("TOUDOU_FOLDER", ""),
FILE_NAME_CSV=os.getenv("FILE_NAME_CSV", "")
)