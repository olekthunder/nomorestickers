from telethon import TelegramClient
from nomorestickers.creds import API_HASH, API_ID


def init_client(
    api_hash: str = API_HASH,
    api_id: int = API_ID
) -> TelegramClient:
    return TelegramClient(
        session="anon", api_hash=api_hash, api_id=api_id
    )
