import time
import win32evtlog
import cv2
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Settings
server = "localhost"
logtype = "Security"
SAVE_FOLDER = r"C:\Users\HASEN\Desktop\IntruderSnap"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Email settings — fill these in
EMAIL_SENDER   = "hasenadem001@gmail.com"
EMAIL_PASSWORD = "dbiu irsr khde lyko"
EMAIL_RECEIVER = "hasenadem002@gmail.com"

flags = (
    win32evtlog.EVENTLOG_BACKWARDS_READ |
    win32evtlog.EVENTLOG_SEQUENTIAL_READ
)

def read_events():
    hand = win32evtlog.OpenEventLog(server, logtype)
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    win32evtlog.CloseEventLog(hand)
    return events

def capture_photo(reason):
    try:
        cam = cv2.VideoCapture(0)
        time.sleep(2)
        for _ in range(10):
            cam.read()
        ret, frame = cam.read()
        cam.release()
        if ret:
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = os.path.join(SAVE_FOLDER, f"{reason}_{ts}.jpg")
            cv2.imwrite(path, frame)
            return path
    except:
        pass
    return None

def send_email(photo_path, reason):
    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = EMAIL_RECEIVER
        msg["Subject"] = "🚨 IntruderSnap Alert — " + reason

        body = f"""
IntruderSnap Security Alert

Event   : {reason}
Time    : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Computer: {os.environ.get("COMPUTERNAME", "Unknown")}

Photo is attached.
        """
        msg.attach(MIMEText(body, "plain"))

        # Attach photo
        if photo_path and os.path.exists(photo_path):
            with open(photo_path, "rb") as f:
                img = MIMEImage(f.read())
                img.add_header("Content-Disposition", "attachment",
                               filename=os.path.basename(photo_path))
                msg.attach(img)

        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

    except Exception as e:
        pass

# Wait for system to load
time.sleep(5)

# Startup photo and email
photo = capture_photo("startup")
send_email(photo, "PC Started")

# Set baseline
events = read_events()
baseline = events[0].RecordNumber if events else 0

# Watch forever
while True:
    try:
        events = read_events()
        for event in events:
            if event.RecordNumber <= baseline:
                break
            if event.EventID == 4625:
                photo = capture_photo("failed_login")
                send_email(photo, "Failed Login Detected")
        if events:
            baseline = max(baseline, events[0].RecordNumber)
    except:
        pass
    time.sleep(1)