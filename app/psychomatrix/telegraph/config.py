from environs import Env

API_URL = "https://api.telegra.ph/{method}/{path}"
BASE_URL = "https://telegra.ph/{endpoint}"
AUTHOR_URL = "https://npsychomatrixbot.t.me/"
AUTHOR_NAME = "Психоматрица [Квадрат Пифагора]"


def get_access_token() -> str:
    env = Env()
    env.read_env()

    return env.str("TELEGRAPH_TOKEN")
