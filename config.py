
from os import environ


class Configs(object):
    API_ID = int(environ.get("API_ID", 0))
    API_HASH = environ.get("API_HASH", "")
    BOT_TOKEN = environ.get("BOT_TOKEN", "")
    OWNER_ID = int(environ.get("OWNER_ID", 0))