# Placemate: Smart Telegram Placement Bot

**Placemate** is an intelligent Telegram bot built with Python and the Telethon library. It listens to real-time chat updates, extracts relevant placement-related information, downloads job-related files, and checks if a student is shortlisted — all automated through one script.

---

## Features

* Real-time Message Listening
  Monitors a specific Telegram group or channel for keywords related to campus drives, hiring, and placements.

* Context-Aware Message Filtering
  Detects and filters drive-related messages using context keywords like “placement”, “hiring”, “shortlist”, etc.

* Document Auto-Downloader
  Automatically downloads Excel files (shortlist) and PDFs (Job Descriptions) posted in the chat.

* Shortlist Checker
  Parses the downloaded Excel file and checks whether specific students are shortlisted using name matching.

---

## Tech Stack

* Python 3.10+
* Telethon – for Telegram API access
* pandas – for Excel file parsing
* openpyxl / xlrd – for Excel compatibility
* dotenv – for environment variable management

---

## Folder Structure

placemate/

├── downloaded\_excel\_files/        → Excel files downloaded from Telegram

├── utils/

│   └── read\_excel.py              → Logic to check if a student is shortlisted

├── .env                           → Stores API credentials and config

├── app.py                         → Main bot logic

├── requirements.txt

└── README.md

---

## Setup Instructions

1. Clone the repository
   git clone [https://github.com/kThendral/placemate.git](https://github.com/kThendral/placemate.git)
   cd placemate

2. Create a virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate (On Windows: venv\Scripts\activate)

3. Install dependencies
   pip install -r requirements.txt

4. Set up your `.env` file
   Create a `.env` file in the root directory and add:
   API\_ID=your\_telegram\_api\_id
   API\_HASH=your\_telegram\_api\_hash
   SESSION\_NAME=placemate\_session
   CHAT\_ID=123456789 (ID of the group/channel to monitor)
   (To get API credentials, visit: [https://my.telegram.org](https://my.telegram.org))

---

## Run the Bot

python app.py

It will:

* Connect to Telegram
* Listen for drive-related messages
* Automatically download relevant Excel/PDF files
* Check if you're shortlisted
* Print results to console

---

## Sample Output

🔗 Connecting to Telegram...
✅ Target chat found: Placement Group 2025
📝 Message: Infosys placement drive this Friday!
🚨 Drive-related message detected!
📄 Document received: infosys\_shortlist.xlsx
📥 Excel file detected: infosys\_shortlist.xlsx
✅ File downloaded to: /downloaded\_excel\_files/infosys\_shortlist.xlsx
📊 Shortlist results:
🎉 Alice Johnson is SHORTLISTED!
❌ Bob Smith is not shortlisted.

---

## Testing

You can manually test it by forwarding placement messages or Excel files to your bot-connected group.

---

## Contributions

Pull requests and feature suggestions are welcome! For major changes, please open an issue first.

---

## License

MIT License. Use freely with credit.

---

## Contact

Maintained by @kThendral @Somnathumapathi
For help or feature requests, please raise an issue on GitHub.


