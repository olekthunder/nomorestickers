from telethon import events

from nomorestickers.client import init_client
from nomorestickers.creds import CHAT_ID

client = init_client()

EXTENSIONS_BLACKLIST = frozenset(('.tgs', '.webp', '.gif', '.mp4'))


@client.on(events.NewMessage(chats=[CHAT_ID], incoming=True))
async def handle_message(event):
    if event.message.file:
        f = event.message.file
        print(f.name)
        print(f.ext)
        if f.ext in EXTENSIONS_BLACKLIST:
            await event.message.delete()


def main():
    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
