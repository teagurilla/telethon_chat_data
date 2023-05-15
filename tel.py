from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
import yaml
import os
import dotenv

dotenv.load_dotenv()
api_id = int(os.environ['api_id'])
api_hash = os.environ['api_hash']

username = os.environ['telegram_username']

with TelegramClient(username, api_id, api_hash) as client:
    result = client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=username,
        limit=500,
        hash=0,
    ))
    messages = []
    titles = 'CS&BA'
    for chat in result.chats:
        if chat.title == titles:
            for i, message in enumerate(client.iter_messages(chat)):
                if message is None:
                    continue
                if message.message is None:
                    continue
                if message.date is None:
                    continue
                if message.id is None:
                    continue
                messages.append({
                    "content": message.message,
                    "date": message.date.timestamp(),
                    "id": message.id,
                    "author": message.from_id and message.from_id.user_id
                })
                print(message.date.strftime('%Y-%m-%d %H:%M:%S'), i, "messages so far", end='\r')
                if not i % 500:
                    yaml.safe_dump(messages, open('messages.yaml', 'w'))
            yaml.safe_dump(messages, open('messages.yaml', 'w'))
