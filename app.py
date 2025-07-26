# print("Hello, World!")
from telethon import TelegramClient, events
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")
chat_id = os.getenv("CHAT_ID")


client = TelegramClient(session_name, api_id, api_hash)

# async def main():
#     async for dialog in client.iter_dialogs():
#         print(dialog.name, dialog.id)
        
# with client:
#     client.loop.run_until_complete(main())


@client.on(events.NewMessage(chats=chat_id))
async def handler(event):
    print(event.message.message)

with client:
    print("🤖 Placemate is now listening for placement updates...")
    client.run_until_disconnected()