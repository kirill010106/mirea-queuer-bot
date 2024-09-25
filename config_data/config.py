from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    bot_token: str
    admin_password: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        TgBot(
            bot_token=env("BOT_TOKEN"),
            admin_password=env("ADMIN_PASSWORD"),
        )
    )