import time
import win32evtlog
import cv2
import os
from datetime import datetime

server = "localhost"
logtype = "Security"

flags = (
    win32evtlog.EVENTLOG_BACKWARDS_READ |
    win32evtlog.EVENTLOG_SEQUENTIAL_READ
)

SAVE_FOLDER = r"C:\Users\HASEN\Desktop\IntruderSnap"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def read_events():
    hand = win32evtlog.OpenEventLog(server, logtype)
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    win32evtlog.CloseEventLog(hand)
    return events

def capture_photo(reason):
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        return
    for _ in range(5):
        camera.read()
    ret, frame = camera.read()
    camera.release()
    if ret:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{reason}_{timestamp}.jpg"
        filepath = os.path.join(SAVE_FOLDER, filename)
        cv2.imwrite(filepath, frame)

# ✅ Take photo immediately when PC starts
capture_photo("startup")

# Set baseline
events = read_events()
baseline_record = events[0].RecordNumber if events else 0

while True:
    try:
        events = read_events()
        for event in events:
            if event.RecordNumber <= baseline_record:
                break
            if event.EventID == 4625:
                capture_photo("failed_login")
        if events:
            baseline_record = max(baseline_record, events[0].RecordNumber)
    except Exception as e:
        pass
    time.sleep(1)