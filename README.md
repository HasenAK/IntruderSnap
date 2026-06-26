# IntruderSnap 🔐📸

A Windows security tool that automatically captures webcam photos and sends email alerts when someone attempts to log in with an incorrect password.

## Features
- ✅ Monitors Windows Security Event Log in real time
- ✅ Detects failed login attempts (Event ID 4625)
- ✅ Captures webcam photo automatically on startup
- ✅ Captures webcam photo on every failed login attempt
- ✅ Sends email alert with photo attached automatically
- ✅ Saves photos with timestamp as evidence
- ✅ Runs silently in background
- ✅ Starts automatically when PC boots

## Requirements
- Windows 10/11
- Python 3.12
- opencv-python
- pywin32

## Installation
1. Clone the repository:
   git clone https://github.com/HasenAK/IntruderSnap.git

2. Install dependencies:
   pip install opencv-python pywin32

3. Set up Gmail App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Create a new app password
   - Copy the 16 character password

4. Edit main.py and fill in your email details:
   EMAIL_SENDER   = "your_gmail@gmail.com"
   EMAIL_PASSWORD = "your_16_char_app_password"
   EMAIL_RECEIVER = "your_gmail@gmail.com"

## Usage
1. Run as Administrator:
   python main.py

2. To build as executable:
   pyinstaller --onefile --hidden-import=win32evtlog --hidden-import=win32api --hidden-import=cv2 main.py

3. To auto start on boot, add to Windows Task Scheduler:
   - Trigger: At log on
   - Action: Run main.exe
   - Check: Run with highest privileges

## How It Works
1. Program starts automatically when PC boots
2. Takes a startup photo immediately
3. Monitors Windows Security Event Log every second
4. When Event ID 4625 is detected (failed login):
   - Captures webcam photo
   - Saves photo with timestamp to IntruderSnap folder
   - Sends email alert with photo attached

## Photos Saved As
- startup_2026-06-24_22-03-45.jpg
- failed_login_2026-06-24_22-05-10.jpg

## Author
HasenAK
