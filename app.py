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

def is_placement_message(message_text):
    MANDATORY_KEYWORDS = {
    "hiring", "recruitment", "placement", "campus drive", "drive", "off-campus", "on-campus", 
    "shortlisted", "interview" , "training period", "ctc", "job", "internship", "stipend",
}
    SUPPORTING_WORDS = {
    "register", "form", "deadline", "apply", "link", "opportunity", "batch", "eligible", "round", "percentage", "criteria", "eligibility", "selection", "form"
}
    UNNECESSARY_WORDS = {
    "webinar", "workshop", "discussion", "seminar", "lecture"
    }

    if any(keyword in message_text for keyword in MANDATORY_KEYWORDS) and any(keyword in message_text for keyword in SUPPORTING_WORDS) and not any(keyword in message_text for keyword in UNNECESSARY_WORDS):
        return True
    return False

def is_job_pdf(message):
    if message.media and message.media.document and message.media.document.mime_type == 'application/pdf':
        if any(word in message.media.document.attributes[0].file_name.lower() for word in {"job", "description", "job-description", "details", "job description"}):
            return True
    return False

@client.on(events.NewMessage(chats=chat_id))
async def handler(event):
    if is_placement_message(event.message.message):
        print("🚨 Drive-related message detected!")
        #send it in group
    if is_job_pdf(event.message):
        print("📄 Job PDF detected!")
        #send it in group

    #excel check shortlisted

with client:
    print("🤖 Placemate is now listening for placement updates...")
    client.run_until_disconnected()