import asyncio
import random

import emoji
from telethon import events

from nomorestickers.client import CLIENT
from nomorestickers.config import (
    CHAT_ID,
    EXTENSIONS_BLACKLIST,
    MAX_DELETE_DELAY,
    MAX_EMOJI_PERCENT,
    MIN_DELETE_DELAY,
    USERNAME_BLACKLIST,
    USER_ID_BLACKLIST,
)
from nomorestickers.event_queue import EVENT_QUEUE


@CLIENT.on(events.NewMessage(chats=[CHAT_ID], incoming=True))
# @CLIENT.on(events.NewMessage(from_users=['me']))
async def handle_message(event):
    # TODO: maybe rewrite this to sync code
    await EVENT_QUEUE.put(event)


def is_user_forbidden(user) -> bool:
    return (
        (user.username and user.username in USERNAME_BLACKLIST)
        or (user.id in USER_ID_BLACKLIST)
    )


def is_emoji_message(message) -> bool:
    if not message.text:
        return False
    total_emoji = 0
    for character in message.text:
        if character in emoji.UNICODE_EMOJI:
            total_emoji += 1
    return (total_emoji / len(message.text)) > MAX_EMOJI_PERCENT


def is_message_file_ext_forbidden(message) -> bool:
    if not message.file or not message.file.ext:
        return False
    return message.file.ext in EXTENSIONS_BLACKLIST


def get_full_name(user) -> str:
    return ' '.join([user.first_name, user.last_name])


async def delete_message(message, log_message):
    await asyncio.sleep(
        random.uniform(MIN_DELETE_DELAY, MAX_DELETE_DELAY)
    )
    await message.delete()
    print(log_message)


async def processor():
    while True:
        event = await EVENT_QUEUE.get()
        message = event.message
        if is_user_forbidden(message.sender):
            reason_to_delete = None
            if message.text and is_emoji_message(message):
                reason_to_delete = 'emoji message'
            elif is_message_file_ext_forbidden(message):
                reason_to_delete = message.file.ext

            if reason_to_delete:
                await delete_message(
                    message,
                    f'Deleted message from {get_full_name(message.sender)}'
                    f' [{reason_to_delete}]'
                )


async def disconnect_handler():
    await CLIENT.disconnected


def main():
    print('Running...')
    CLIENT.start()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(
            processor(),
            disconnect_handler()
        ))
    except KeyboardInterrupt:
        pass
    finally:
        CLIENT.disconnect()


if __name__ == "__main__":
    main()
