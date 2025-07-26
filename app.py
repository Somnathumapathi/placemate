from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
from utils.read_excel import is_person_shortlisted

# Load environment variables from .env file
load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")
chat_id = int(os.getenv("CHAT_ID"))  # Convert to integer

# Initialize the Telegram client
client = TelegramClient(session_name, api_id, api_hash)

# Create directory for downloaded Excel files
download_dir = "downloaded_excel_files"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

placement_context_active = False

# Connection establishment and chat discovery
async def main():
    print("🔗 Connecting to Telegram...")
    await client.start()
    
    print("📋 Available chats:")
    async for dialog in client.iter_dialogs():
        print(f"Chat: {dialog.name} | ID: {dialog.id}")
    
    # Get and cache the target chat entity
    try:
        chat_entity = await client.get_entity(chat_id)
        print(f"✅ Target chat found: {chat_entity.title if hasattr(chat_entity, 'title') else 'Private Chat'}")
    except Exception as e:
        print(f"❌ Error getting chat entity: {e}")
        print("Please check your CHAT_ID in the .env file")
        return

def is_placement_message(message_text):
    MANDATORY_KEYWORDS = {
        "hiring", "recruitment", "placement", "campus drive", "drive", "off-campus", "on-campus", 
        "shortlisted", "interview", "training period", "ctc", "job", "internship", "stipend"
    }
    SUPPORTING_WORDS = {
        "register", "form", "deadline", "apply", "link", "opportunity", "batch", "eligible", "round", "percentage", "criteria", "eligibility", "selection", "form"
    }
    UNNECESSARY_WORDS = {
        "webinar", "workshop", "discussion", "seminar", "lecture"
    }

    message_text = message_text.lower()
    if any(keyword in message_text for keyword in MANDATORY_KEYWORDS) and \
       any(keyword in message_text for keyword in SUPPORTING_WORDS) and \
       not any(keyword in message_text for keyword in UNNECESSARY_WORDS):
        return True
    return False

def is_job_pdf(message):
    if message.media and message.media.document and message.media.document.mime_type == 'application/pdf':
        if hasattr(message.media.document, 'attributes'):
            for attr in message.media.document.attributes:
                if hasattr(attr, 'file_name') and any(
                    word in attr.file_name.lower() for word in {"job", "description", "job-description", "details", "job description"}
                ):
                    return True
    return False


@client.on(events.NewMessage(chats=chat_id))
async def handler(event):
    global placement_context_active

    if event.message.message:
        print(f"📝 Message: {event.message.message}")

    keyWords = ["placement", "placed", "placement update", 'drive', 'hiring', 'shortlist', 'company']
    if event.message.message and any(keyword in event.message.message.lower() for keyword in keyWords):
        print("🚨 Drive-related message detected!")
        placement_context_active = True
    
    if is_job_pdf(event.message):
        print("📄 Job description PDF detected!")

    if event.message.document:
        try:
            file_name = None
            if event.message.document.attributes:
                for attr in event.message.document.attributes:
                    if hasattr(attr, 'file_name'):
                        file_name = attr.file_name
                        break
            
            if not file_name:
                file_name = f"document_{event.message.document.id}"
            print(f"📄 Document received: {file_name}")

            # Check if the file is an Excel file
            if file_name and file_name.endswith(('.xlsx', '.xls')):
                print(f"📥 Excel file detected: {file_name}")
                # Download the file
                file_path = await client.download_media(
                    event.message.document, 
                    file=os.path.join(download_dir, file_name)
                )
                print(f"✅ File downloaded to: {file_path}")

                if placement_context_active:
                    print("🔍 Processing placement-related Excel file...")
                    results = is_person_shortlisted(download_dir)
                    print(f"📊 Shortlist results: {results}")
                    
                    # Send notification for shortlisted people
                    for name, is_shortlisted in results.items():
                        if is_shortlisted:
                            print(f"🎉 {name} is SHORTLISTED!")
                        else:
                            print(f"❌ {name} is not shortlisted.")
                    
                    # Reset context after processing
                    placement_context_active = False

        except Exception as e:
            print(f"❌ Error while processing document: {e}")

async def run_bot():
    async with client:
        # Initialize connection and cache entities
        await main()
        
        print("🤖 Placemate is now listening for placement updates...")
        print(f"📁 Excel files will be saved to: {os.path.abspath(download_dir)}")
        
        # Keep the client running
        await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_bot())